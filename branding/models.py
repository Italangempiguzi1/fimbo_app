from django.db import models
from django.utils import timezone
from core.models import TimeStampedUUIDModel


class BrandPlacement(TimeStampedUUIDModel):
    class Placement(models.TextChoices):
        HOME_CAROUSEL = 'home_carousel', 'Home Carousel'
        REELS_TOP = 'reels_top', 'Reels Top'
        PLAYER_SIDE = 'player_side', 'Player Side'

    title = models.CharField(max_length=160)
    subtitle = models.CharField(max_length=240, blank=True)
    image_url = models.URLField(blank=True)
    image_file = models.ImageField(upload_to='branding/', null=True, blank=True)
    link_url = models.URLField(blank=True)
    placement = models.CharField(max_length=40, choices=Placement.choices, default=Placement.HOME_CAROUSEL)
    sort_order = models.PositiveIntegerField(default=0)
    starts_at = models.DateTimeField(null=True, blank=True)
    ends_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['sort_order', '-created_at']

    @property
    def image(self):
        if self.image_file:
            return self.image_file.url
        return self.image_url

    @property
    def is_live(self):
        now = timezone.now()
        return self.is_active and (self.starts_at is None or self.starts_at <= now) and (self.ends_at is None or self.ends_at >= now)

    def __str__(self):
        return self.title
