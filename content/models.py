from django.db import models
from django.utils.text import slugify
from core.models import TimeStampedUUIDModel


class Category(TimeStampedUUIDModel):
    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'categories'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Content(TimeStampedUUIDModel):
    class ContentType(models.TextChoices):
        MOVIE = 'movie', 'Movie'
        SERIES = 'series', 'TV Series'
        DOCUMENTARY = 'documentary', 'Documentary'
        EDUCATIONAL = 'educational', 'Educational'
        SPORT = 'sport', 'Sports'
        KIDS = 'kids', 'Kids'
        NEWS = 'news', 'News'
        PREMIUM_CREATOR = 'premium_creator', 'Premium Creator Content'
        OTHER = 'other', 'Other'

    class Status(models.TextChoices):
        DRAFT = 'draft', 'Draft'
        PROCESSING = 'processing', 'Processing'
        PENDING_REVIEW = 'pending_review', 'Pending Review'
        APPROVED = 'approved', 'Approved'
        REJECTED = 'rejected', 'Rejected'
        ARCHIVED = 'archived', 'Archived'

    creator = models.ForeignKey('creators.CreatorProfile', on_delete=models.CASCADE, related_name='contents')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name='contents', null=True, blank=True)
    title = models.CharField(max_length=220)
    slug = models.SlugField(max_length=240, blank=True)
    description = models.TextField(blank=True)
    content_type = models.CharField(max_length=30, choices=ContentType.choices)
    language = models.CharField(max_length=50, default='Swahili')
    age_rating = models.CharField(max_length=20, default='General')
    release_year = models.PositiveIntegerField(null=True, blank=True)
    season_number = models.PositiveIntegerField(null=True, blank=True)
    episode_number = models.PositiveIntegerField(null=True, blank=True)
    thumbnail_url = models.URLField(blank=True)
    poster_url = models.URLField(blank=True)
    banner_image_url = models.URLField(blank=True)
    trailer_url = models.URLField(blank=True)
    thumbnail_file = models.ImageField(upload_to='content/thumbnails/', null=True, blank=True)
    banner_file = models.ImageField(upload_to='content/banners/', null=True, blank=True)
    source_video_file = models.FileField(upload_to='content/source/', null=True, blank=True)
    duration_seconds = models.PositiveIntegerField(default=0)
    is_premium = models.BooleanField(default=True)
    early_access = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    is_trending = models.BooleanField(default=False)
    status = models.CharField(max_length=30, choices=Status.choices, default=Status.DRAFT)
    published_at = models.DateTimeField(null=True, blank=True)
    total_views = models.PositiveIntegerField(default=0)
    total_watch_seconds = models.PositiveBigIntegerField(default=0)
    total_likes = models.PositiveIntegerField(default=0)
    total_comments = models.PositiveIntegerField(default=0)
    total_votes = models.PositiveIntegerField(default=0)
    total_awards = models.PositiveIntegerField(default=0)
    completion_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    recommendation_score = models.DecimalField(max_digits=12, decimal_places=4, default=0)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', 'content_type', 'created_at']),
            models.Index(fields=['status', 'is_featured', 'created_at']),
            models.Index(fields=['status', 'is_trending', 'recommendation_score']),
            models.Index(fields=['creator', 'status']),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)[:230]
        super().save(*args, **kwargs)

    @property
    def thumbnail(self):
        if self.thumbnail_file:
            return self.thumbnail_file.url
        return self.thumbnail_url

    @property
    def banner_image(self):
        if self.banner_file:
            return self.banner_file.url
        return self.banner_image_url or self.poster_url or self.thumbnail

    def __str__(self):
        return self.title


class VideoAsset(TimeStampedUUIDModel):
    class ProcessingStatus(models.TextChoices):
        UPLOADED = 'uploaded', 'Uploaded'
        PROCESSING = 'processing', 'Processing'
        READY = 'ready', 'Ready'
        FAILED = 'failed', 'Failed'

    content = models.OneToOneField(Content, on_delete=models.CASCADE, related_name='video_asset')
    source_file_url = models.URLField(blank=True)
    hls_manifest_url = models.URLField(blank=True)
    dash_manifest_url = models.URLField(blank=True)
    mp4_url = models.URLField(blank=True)
    local_hls_path = models.CharField(max_length=500, blank=True)
    quality_label = models.CharField(max_length=30, default='720p')
    file_size_mb = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    drm_license_url = models.URLField(blank=True)
    watermark_text = models.CharField(max_length=120, blank=True)
    processing_status = models.CharField(max_length=20, choices=ProcessingStatus.choices, default=ProcessingStatus.UPLOADED)
    processing_error = models.TextField(blank=True)

    def __str__(self):
        return f'VideoAsset for {self.content.title}'
