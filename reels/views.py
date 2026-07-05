from django.db.models import Q
from django.utils import timezone
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.response import Response
from core.permissions import IsCreator
from subscriptions.services import has_active_subscription
from recommendations.services import ranked_reels_queryset
from media_pipeline.tasks import process_reel_video
from .models import Reel
from .serializers import ReelSerializer


class ReelViewSet(viewsets.ModelViewSet):
    serializer_class = ReelSerializer
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get_queryset(self):
        user = self.request.user
        qs = Reel.objects.select_related('creator', 'category')
        if user.is_authenticated and user.is_staff:
            return qs
        if user.is_authenticated and hasattr(user, 'creator_profile'):
            return qs.filter(Q(status=Reel.Status.APPROVED) | Q(creator=user.creator_profile))
        return qs.filter(status=Reel.Status.APPROVED)

    def get_permissions(self):
        if self.action in {'feed', 'list', 'retrieve'}:
            return [permissions.AllowAny()]
        if self.action in {'create', 'update', 'partial_update', 'destroy', 'submit_for_review'}:
            return [permissions.IsAuthenticated(), IsCreator()]
        if self.action in {'approve', 'reject'}:
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        creator = self.request.user.creator_profile
        if not creator.can_upload:
            raise PermissionDenied('Only verified creators are allowed to upload reels.')
        status_value = Reel.Status.PROCESSING if self.request.FILES.get('video_file') else Reel.Status.DRAFT
        reel = serializer.save(creator=creator, status=status_value)
        if reel.video_file:
            process_reel_video.delay(str(reel.id))

    @action(detail=False, methods=['get'])
    def feed(self, request):
        qs = Reel.objects.filter(status=Reel.Status.APPROVED).select_related('creator', 'category')
        qs = ranked_reels_queryset(qs, request.user if request.user.is_authenticated else None)
        page = self.paginate_queryset(qs)
        serializer = self.get_serializer(page or qs, many=True, context={'request': request})
        if page is not None:
            return self.get_paginated_response(serializer.data)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def submit_for_review(self, request, pk=None):
        reel = self.get_object()
        if not request.user.is_staff and reel.creator.user != request.user:
            return Response({'detail': 'Not allowed.'}, status=status.HTTP_403_FORBIDDEN)
        reel.status = Reel.Status.PENDING_REVIEW
        reel.save(update_fields=['status', 'updated_at'])
        return Response(ReelSerializer(reel, context={'request': request}).data)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def approve(self, request, pk=None):
        reel = self.get_object()
        reel.status = Reel.Status.APPROVED
        reel.published_at = timezone.now()
        reel.save(update_fields=['status', 'published_at', 'updated_at'])
        return Response(ReelSerializer(reel, context={'request': request}).data)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def reject(self, request, pk=None):
        reel = self.get_object()
        reel.status = Reel.Status.REJECTED
        reel.save(update_fields=['status', 'updated_at'])
        return Response(ReelSerializer(reel, context={'request': request}).data)

    @action(detail=True, methods=['get'])
    def stream(self, request, pk=None):
        reel = self.get_object()
        if reel.status != Reel.Status.APPROVED and not request.user.is_staff:
            return Response({'detail': 'Reel is not available.'}, status=404)
        if not has_active_subscription(request.user):
            return Response({
                'detail': 'Active subscription required.',
                'code': 'subscription_required',
                'redirect_to': '/subscriptions',
            }, status=status.HTTP_402_PAYMENT_REQUIRED)
        return Response({
            'reel_id': str(reel.id),
            'title': reel.title,
            'hls_manifest_url': reel.hls_manifest_url,
            'video_url': reel.video_url or (reel.video_file.url if reel.video_file else ''),
        })

    @action(detail=True, methods=['post'])
    def share(self, request, pk=None):
        reel = self.get_object()
        reel.total_shares = reel.total_shares + 1
        reel.save(update_fields=['total_shares', 'updated_at'])
        return Response({'share_url': f"umbrella://reels/{reel.id}", 'total_shares': reel.total_shares})
