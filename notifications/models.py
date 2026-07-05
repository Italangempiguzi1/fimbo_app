from django.conf import settings
from django.db import models
from core.models import TimeStampedUUIDModel


class Notification(TimeStampedUUIDModel):
    class NotificationType(models.TextChoices):
        SYSTEM = 'system', 'System'
        SUBSCRIPTION = 'subscription', 'Subscription'
        CREATOR = 'creator', 'Creator'
        CONTENT = 'content', 'Content'
        REWARD = 'reward', 'Reward'
        MODERATION = 'moderation', 'Moderation'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=30, choices=NotificationType.choices, default=NotificationType.SYSTEM)
    title = models.CharField(max_length=180)
    body = models.TextField(blank=True)
    data = models.JSONField(default=dict, blank=True)
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [models.Index(fields=['user', 'is_read', 'created_at'])]

    def __str__(self):
        return self.title
