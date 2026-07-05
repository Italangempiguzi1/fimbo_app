from rest_framework import serializers
from content.serializers import ContentSerializer
from .models import DownloadLicense

class DownloadLicenseSerializer(serializers.ModelSerializer):
    content_detail = ContentSerializer(source='content', read_only=True)
    is_valid = serializers.BooleanField(read_only=True)
    class Meta:
        model = DownloadLicense
        fields = ('id', 'content', 'content_detail', 'license_token', 'expires_at', 'status', 'local_asset_key', 'is_valid', 'created_at')
        read_only_fields = ('id', 'license_token', 'expires_at', 'status', 'created_at')
