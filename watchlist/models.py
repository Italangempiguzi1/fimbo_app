from django.conf import settings
from django.db import models
from core.models import TimeStampedUUIDModel


class WatchlistItem(TimeStampedUUIDModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='watchlist_items')
    content = models.ForeignKey('content.Content', on_delete=models.CASCADE, related_name='watchlisted_by')

    class Meta:
        unique_together = ('user', 'content')
        ordering = ['-created_at']
