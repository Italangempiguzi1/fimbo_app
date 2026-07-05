from rest_framework import serializers
from .models import CreatorProfile


class CreatorProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    is_verified = serializers.BooleanField(read_only=True)

    class Meta:
        model = CreatorProfile
        fields = (
            'id', 'user', 'username', 'email', 'display_name', 'bio', 'profile_image_url',
            'cover_image_url', 'business_name', 'content_focus', 'verification_status',
            'is_verified', 'payout_phone', 'bank_name', 'bank_account_name',
            'bank_account_number', 'total_followers', 'total_views', 'total_likes',
            'total_votes', 'total_awards', 'total_watch_seconds', 'is_active',
            'created_at', 'updated_at'
        )
        read_only_fields = (
            'id', 'user', 'verification_status', 'total_followers', 'total_views',
            'total_likes', 'total_votes', 'total_awards', 'total_watch_seconds',
            'is_active', 'created_at', 'updated_at'
        )
