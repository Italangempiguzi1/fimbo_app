from rest_framework import serializers
from content.serializers import ContentSerializer
from .models import WatchlistItem

class WatchlistItemSerializer(serializers.ModelSerializer):
    content_detail = ContentSerializer(source='content', read_only=True)
    class Meta:
        model = WatchlistItem
        fields = ('id', 'content', 'content_detail', 'created_at')
        read_only_fields = ('id', 'created_at')
