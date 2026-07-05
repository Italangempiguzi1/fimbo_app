from rest_framework import serializers
from subscriptions.services import has_active_subscription
from .models import Reel


class ReelSerializer(serializers.ModelSerializer):
    creator_name = serializers.CharField(source='creator.display_name', read_only=True)
    creator_verified = serializers.BooleanField(source='creator.is_verified', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    thumbnail = serializers.CharField(read_only=True)
    can_stream = serializers.SerializerMethodField()
    stream_url = serializers.SerializerMethodField()

    class Meta:
        model = Reel
        fields = (
            'id', 'creator', 'creator_name', 'creator_verified', 'category', 'category_name',
            'title', 'caption', 'video_url', 'hls_manifest_url', 'thumbnail_url', 'video_file',
            'thumbnail_file', 'thumbnail', 'duration_seconds', 'is_shareable', 'status',
            'published_at', 'total_views', 'total_watch_seconds', 'total_likes', 'total_comments',
            'total_votes', 'total_awards', 'total_shares', 'completion_rate', 'recommendation_score',
            'can_stream', 'stream_url', 'created_at', 'updated_at'
        )
        read_only_fields = (
            'id', 'creator', 'status', 'published_at', 'total_views', 'total_watch_seconds',
            'total_likes', 'total_comments', 'total_votes', 'total_awards', 'total_shares',
            'completion_rate', 'recommendation_score', 'created_at', 'updated_at'
        )

    def get_can_stream(self, obj):
        request = self.context.get('request')
        return bool(request and request.user and request.user.is_authenticated and has_active_subscription(request.user))

    def get_stream_url(self, obj):
        request = self.context.get('request')
        if request and request.user and request.user.is_authenticated and has_active_subscription(request.user):
            return obj.stream_url
        return ''
