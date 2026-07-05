from django.db.models import Q
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from branding.models import BrandPlacement
from branding.serializers import BrandPlacementSerializer
from content.models import Content
from content.serializers import ContentSerializer
from recommendations.services import ranked_content_queryset
from .models import HeroBanner, HomeSection
from .serializers import HeroBannerSerializer


def section_queryset(section, user):
    qs = Content.objects.filter(status=Content.Status.APPROVED).select_related('creator', 'category', 'video_asset')
    if section.category_id:
        qs = qs.filter(category=section.category)
    if section.content_type:
        qs = qs.filter(content_type=section.content_type)
    if section.section_kind == HomeSection.SectionKind.FEATURED:
        qs = qs.filter(is_featured=True).order_by('-recommendation_score', '-published_at')
    elif section.section_kind == HomeSection.SectionKind.NEW_ARRIVALS:
        qs = qs.order_by('-published_at', '-created_at')
    elif section.section_kind == HomeSection.SectionKind.POPULAR:
        qs = qs.order_by('-total_views', '-total_watch_seconds')
    elif section.section_kind == HomeSection.SectionKind.TRENDING:
        qs = qs.filter(Q(is_trending=True) | Q(recommendation_score__gt=0)).order_by('-recommendation_score', '-created_at')
    else:
        qs = ranked_content_queryset(qs, user)
    return qs[:section.item_limit]


class HomeAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        user = request.user if request.user.is_authenticated else None
        banners = HeroBanner.objects.filter(is_active=True).select_related('content', 'reel')[:10]
        brands = BrandPlacement.objects.filter(is_active=True, placement=BrandPlacement.Placement.HOME_CAROUSEL)[:12]
        sections_payload = []
        sections = HomeSection.objects.filter(is_active=True).select_related('category')
        if not sections.exists():
            defaults = [
                ('featured', 'Featured', HomeSection.SectionKind.FEATURED),
                ('new_arrivals', 'New Arrivals', HomeSection.SectionKind.NEW_ARRIVALS),
                ('popular', 'Popular', HomeSection.SectionKind.POPULAR),
                ('trending', 'Trending', HomeSection.SectionKind.TRENDING),
                ('recommended', 'Recommended for You', HomeSection.SectionKind.RECOMMENDED),
            ]
            sections = [HomeSection(key=k, title=t, section_kind=s, item_limit=12) for k, t, s in defaults]
        for section in sections:
            items = ContentSerializer(section_queryset(section, user), many=True, context={'request': request}).data
            sections_payload.append({
                'id': str(getattr(section, 'id', '')),
                'key': section.key,
                'title': section.title,
                'section_kind': section.section_kind,
                'view_all_url': f'/api/content/items/view-all/?section={section.key}',
                'items': items,
            })
        return Response({
            'tabs': [
                {'key': 'all', 'label': 'All'}, {'key': 'movie', 'label': 'Movies'},
                {'key': 'series', 'label': 'TV Shows'}, {'key': 'sport', 'label': 'Sports'},
                {'key': 'kids', 'label': 'Kids'}, {'key': 'news', 'label': 'News'},
                {'key': 'other', 'label': 'Others'},
            ],
            'hero_banners': HeroBannerSerializer(banners, many=True).data,
            'branding': BrandPlacementSerializer(brands, many=True).data,
            'sections': sections_payload,
        })
