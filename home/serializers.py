from rest_framework import serializers
from branding.serializers import BrandPlacementSerializer
from content.serializers import ContentSerializer
from .models import HeroBanner, HomeSection


class HeroBannerSerializer(serializers.ModelSerializer):
    image = serializers.CharField(read_only=True)

    class Meta:
        model = HeroBanner
        fields = '__all__'


class HomeSectionSerializer(serializers.ModelSerializer):
    items = serializers.ListField(read_only=True)

    class Meta:
        model = HomeSection
        fields = ('id', 'key', 'title', 'section_kind', 'category', 'content_type', 'sort_order', 'item_limit', 'items')
