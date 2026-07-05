import uuid
from datetime import timedelta
from django.conf import settings
from django.db import models
from django.utils import timezone
from core.models import TimeStampedUUIDModel


class DownloadLicense(TimeStampedUUIDModel):
    class Status(models.TextChoices):
        ACTIVE = 'active', 'Active'
        EXPIRED = 'expired', 'Expired'
        REVOKED = 'revoked', 'Revoked'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='download_licenses')
    content = models.ForeignKey('content.Content', on_delete=models.CASCADE, related_name='download_licenses')
    license_token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    expires_at = models.DateTimeField(timezone.now() + timedelta(days=30))
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE)
    local_asset_key = models.CharField(max_length=240, blank=True)

    class Meta:
        unique_together = ('user', 'content')
        ordering = ['-created_at']

    @property
    def is_valid(self):
        return self.status == self.Status.ACTIVE and self.expires_at >= timezone.now()
