import uuid
from django.conf import settings
from django.db import models
from django.utils import timezone
from core.models import TimeStampedUUIDModel
from engagement.models import TargetType


class WatchSession(TimeStampedUUIDModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='watch_sessions')
    creator = models.ForeignKey('creators.CreatorProfile', on_delete=models.SET_NULL, related_name='watch_sessions', null=True, blank=True)
    target_type = models.CharField(max_length=20, choices=TargetType.choices)
    target_id = models.UUIDField(default=uuid.uuid4)
    started_at = models.DateTimeField(default=timezone.now)
    ended_at = models.DateTimeField(null=True, blank=True)
    seconds_watched = models.PositiveIntegerField(default=0)
    completed = models.BooleanField(default=False)
    device_id = models.CharField(max_length=120, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    is_valid_view = models.BooleanField(default=False)

    class Meta:
        ordering = ['-started_at']
        indexes = [
            models.Index(fields=['creator', 'target_type', 'started_at']),
            models.Index(fields=['user', 'target_type', 'started_at']),
            models.Index(fields=['is_valid_view', 'started_at']),
        ]

    def mark_ended(self, seconds_watched, completed=False):
        self.ended_at = timezone.now()
        self.seconds_watched = max(int(seconds_watched), 0)
        self.completed = completed
        self.is_valid_view = self.seconds_watched >= 10
        self.save(update_fields=['ended_at', 'seconds_watched', 'completed', 'is_valid_view', 'updated_at'])
