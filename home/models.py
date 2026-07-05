from django.db import models
from core.models import TimeStampedUUIDModel


class HeroBanner(TimeStampedUUIDModel):
    class TargetType(models.TextChoices):
        CONTENT = 'content', 'Content'
        REEL = 'reel', 'Reel'
        EXTERNAL = 'external', 'External Link'

    title = models.CharField(max_length=180)
    subtitle = models.CharField(max_length=240, blank=True)
    image_url = models.URLField(blank=True)
    image_file = models.ImageField(upload_to='home/banners/', null=True, blank=True)
    target_type = models.CharField(max_length=20, choices=TargetType.choices, default=TargetType.CONTENT)
    content = models.ForeignKey('content.Content', null=True, blank=True, on_delete=models.SET_NULL, related_name='hero_banners')
    reel = models.ForeignKey('reels.Reel', null=True, blank=True, on_delete=models.SET_NULL, related_name='hero_banners')
    external_url = models.URLField(blank=True)
    sort_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['sort_order', '-created_at']

    @property
    def image(self):
        if self.image_file:
            return self.image_file.url
        return self.image_url or (self.content.banner_image if self.content else '')

    def __str__(self):
        return self.title


class HomeSection(TimeStampedUUIDModel):
    class SectionKind(models.TextChoices):
        FEATURED = 'featured', 'Featured'
        NEW_ARRIVALS = 'new_arrivals', 'New Arrivals'
        POPULAR = 'popular', 'Popular'
        TRENDING = 'trending', 'Trending'
        RECOMMENDED = 'recommended', 'Recommended'
        CONTINUE_WATCHING = 'continue_watching', 'Continue Watching'
        CATEGORY = 'category', 'Category'

    key = models.SlugField(unique=True)
    title = models.CharField(max_length=120)
    section_kind = models.CharField(max_length=40, choices=SectionKind.choices)
    category = models.ForeignKey('content.Category', null=True, blank=True, on_delete=models.SET_NULL)
    content_type = models.CharField(max_length=30, blank=True)
    sort_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    item_limit = models.PositiveIntegerField(default=12)

    class Meta:
        ordering = ['sort_order', 'title']

    def __str__(self):
        return self.title
