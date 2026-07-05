from rest_framework import serializers
from subscriptions.services import has_active_subscription
from .models import Category, Content, VideoAsset


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'slug', 'description', 'is_active')
        read_only_fields = ('id',)


class VideoAssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoAsset
        fields = (
            'id', 'source_file_url', 'hls_manifest_url', 'dash_manifest_url', 'mp4_url',
            'local_hls_path', 'quality_label', 'file_size_mb', 'drm_license_url',
            'watermark_text', 'processing_status', 'processing_error'
        )
        read_only_fields = ('id', 'processing_status', 'processing_error')


class ContentSerializer(serializers.ModelSerializer):
    creator_name = serializers.CharField(source='creator.display_name', read_only=True)
    creator_verified = serializers.BooleanField(source='creator.is_verified', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    video_asset = VideoAssetSerializer(read_only=True)
    thumbnail = serializers.CharField(read_only=True)
    banner_image = serializers.CharField(read_only=True)
    can_stream = serializers.SerializerMethodField()

    class Meta:
        model = Content
        fields = (
            'id', 'creator', 'creator_name', 'creator_verified', 'category', 'category_name',
            'title', 'slug', 'description', 'content_type', 'language', 'age_rating',
            'release_year', 'season_number', 'episode_number', 'thumbnail_url', 'poster_url',
            'banner_image_url', 'trailer_url', 'thumbnail_file', 'banner_file', 'source_video_file',
            'thumbnail', 'banner_image', 'duration_seconds', 'is_premium', 'early_access',
            'is_featured', 'is_trending', 'status', 'published_at', 'total_views',
            'total_watch_seconds', 'total_likes', 'total_comments', 'total_votes',
            'total_awards', 'completion_rate', 'recommendation_score', 'video_asset',
            'can_stream', 'created_at', 'updated_at'
        )
        read_only_fields = (
            'id', 'creator', 'slug', 'status', 'published_at', 'total_views', 'total_watch_seconds',
            'total_likes', 'total_comments', 'total_votes', 'total_awards', 'completion_rate',
            'recommendation_score', 'created_at', 'updated_at'
        )

    def get_can_stream(self, obj):
        request = self.context.get('request')
        return bool(request and request.user and request.user.is_authenticated and has_active_subscription(request.user))


class ContentCreateSerializer(serializers.ModelSerializer):
    source_file_url = serializers.URLField(required=False, allow_blank=True, write_only=True)
    hls_manifest_url = serializers.URLField(required=False, allow_blank=True, write_only=True)
    mp4_url = serializers.URLField(required=False, allow_blank=True, write_only=True)
    quality_label = serializers.CharField(required=False, default='720p', write_only=True)

    class Meta:
        model = Content
        fields = (
            'id', 'category', 'title', 'description', 'content_type', 'language', 'age_rating',
            'release_year', 'season_number', 'episode_number', 'thumbnail_url', 'poster_url',
            'banner_image_url', 'trailer_url', 'thumbnail_file', 'banner_file', 'source_video_file',
            'duration_seconds', 'is_premium', 'early_access', 'is_featured', 'is_trending',
            'source_file_url', 'hls_manifest_url', 'mp4_url', 'quality_label'
        )
        read_only_fields = ('id',)

    def create(self, validated_data):
        asset_data = {
            'source_file_url': validated_data.pop('source_file_url', ''),
            'hls_manifest_url': validated_data.pop('hls_manifest_url', ''),
            'mp4_url': validated_data.pop('mp4_url', ''),
            'quality_label': validated_data.pop('quality_label', '720p'),
        }
        source_file = validated_data.get('source_video_file')
        if source_file and not asset_data['source_file_url']:
            # During development, MEDIA_URL will serve this. In production this should become an S3/CDN URL.
            asset_data['source_file_url'] = ''
        content = Content.objects.create(**validated_data)
        if source_file and not asset_data['mp4_url']:
            asset_data['mp4_url'] = content.source_video_file.url if content.source_video_file else ''
        VideoAsset.objects.create(content=content, **asset_data)
        return content
