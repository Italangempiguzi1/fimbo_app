from django.db.models import Q
from django.utils import timezone
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.response import Response
from core.permissions import IsCreator
from subscriptions.services import has_active_subscription
from recommendations.services import ranked_content_queryset
from media_pipeline.tasks import process_content_video
from .models import Category, Content
from .serializers import CategorySerializer, ContentCreateSerializer, ContentSerializer


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'slug'


class ContentViewSet(viewsets.ModelViewSet):
    serializer_class = ContentSerializer
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get_queryset(self):
        user = self.request.user
        qs = Content.objects.select_related('creator', 'category', 'video_asset')
        if user.is_authenticated and user.is_staff:
            return qs
        if user.is_authenticated and hasattr(user, 'creator_profile'):
            return qs.filter(Q(status=Content.Status.APPROVED) | Q(creator=user.creator_profile))
        return qs.filter(status=Content.Status.APPROVED)

    def get_serializer_class(self):
        if self.action in {'create', 'update', 'partial_update'}:
            return ContentCreateSerializer
        return ContentSerializer

    def get_permissions(self):
        if self.action in {'list', 'retrieve', 'tabs', 'view_all'}:
            return [permissions.AllowAny()]
        if self.action in {'create', 'update', 'partial_update', 'destroy', 'submit_for_review'}:
            return [permissions.IsAuthenticated(), IsCreator()]
        if self.action in {'approve', 'reject'}:
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        creator = self.request.user.creator_profile
        if not creator.can_upload:
            raise PermissionDenied('Only verified creators are allowed to upload content.')
        status_value = Content.Status.PROCESSING if self.request.FILES.get('source_video_file') else Content.Status.DRAFT
        content = serializer.save(creator=creator, status=status_value)
        if content.source_video_file:
            process_content_video.delay(str(content.id))

    @action(detail=False, methods=['get'], permission_classes=[permissions.AllowAny])
    def tabs(self, request):
        return Response([
            {'key': 'all', 'label': 'All'},
            {'key': 'movie', 'label': 'Movies'},
            {'key': 'series', 'label': 'TV Shows'},
            {'key': 'sport', 'label': 'Sports'},
            {'key': 'kids', 'label': 'Kids'},
            {'key': 'news', 'label': 'News'},
            {'key': 'other', 'label': 'Others'},
        ])

    @action(detail=False, methods=['get'], url_path='view-all', permission_classes=[permissions.AllowAny])
    def view_all(self, request):
        qs = Content.objects.filter(status=Content.Status.APPROVED).select_related('creator', 'category', 'video_asset')
        section = request.query_params.get('section', '')
        category = request.query_params.get('category', '')
        content_type = request.query_params.get('content_type', '')
        sort = request.query_params.get('sort', 'recommended')
        if category:
            qs = qs.filter(category__slug=category)
        if content_type and content_type != 'all':
            qs = qs.filter(content_type=content_type)
        if section == 'new_arrivals':
            qs = qs.order_by('-published_at', '-created_at')
        elif section == 'popular':
            qs = qs.order_by('-total_views', '-total_watch_seconds')
        elif section == 'trending':
            qs = qs.filter(is_trending=True).order_by('-recommendation_score', '-created_at')
        elif section == 'featured':
            qs = qs.filter(is_featured=True).order_by('-recommendation_score', '-created_at')
        elif sort == 'top_rated':
            qs = qs.order_by('-total_votes', '-completion_rate')
        else:
            qs = ranked_content_queryset(qs, request.user if request.user.is_authenticated else None)
        page = self.paginate_queryset(qs)
        serializer = ContentSerializer(page or qs, many=True, context={'request': request})
        if page is not None:
            return self.get_paginated_response(serializer.data)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def submit_for_review(self, request, pk=None):
        content = self.get_object()
        if not request.user.is_staff and content.creator.user != request.user:
            return Response({'detail': 'Not allowed.'}, status=status.HTTP_403_FORBIDDEN)
        content.status = Content.Status.PENDING_REVIEW
        content.save(update_fields=['status', 'updated_at'])
        return Response(ContentSerializer(content, context={'request': request}).data)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def approve(self, request, pk=None):
        content = self.get_object()
        content.status = Content.Status.APPROVED
        content.published_at = timezone.now()
        content.save(update_fields=['status', 'published_at', 'updated_at'])
        return Response(ContentSerializer(content, context={'request': request}).data)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def reject(self, request, pk=None):
        content = self.get_object()
        content.status = Content.Status.REJECTED
        content.save(update_fields=['status', 'updated_at'])
        return Response(ContentSerializer(content, context={'request': request}).data)

    @action(detail=True, methods=['get'])
    def stream(self, request, pk=None):
        content = self.get_object()
        if content.status != Content.Status.APPROVED and not request.user.is_staff:
            return Response({'detail': 'Content is not available.'}, status=404)
        if not has_active_subscription(request.user):
            return Response({
                'detail': 'Active subscription required.',
                'code': 'subscription_required',
                'redirect_to': '/subscriptions',
            }, status=status.HTTP_402_PAYMENT_REQUIRED)
        asset = getattr(content, 'video_asset', None)
        if not asset:
            return Response({'detail': 'Video asset is not ready yet.'}, status=404)
        return Response({
            'content_id': str(content.id),
            'title': content.title,
            'hls_manifest_url': asset.hls_manifest_url,
            'dash_manifest_url': asset.dash_manifest_url,
            'mp4_url': asset.mp4_url,
            'quality_label': asset.quality_label,
            'drm_license_url': asset.drm_license_url,
            'watermark_text': asset.watermark_text or request.user.email,
        })
