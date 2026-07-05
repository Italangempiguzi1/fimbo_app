from django.db import models
from core.models import TimeStampedUUIDModel


class Reel(TimeStampedUUIDModel):
    class Status(models.TextChoices):
        DRAFT = 'draft', 'Draft'
        PROCESSING = 'processing', 'Processing'
        PENDING_REVIEW = 'pending_review', 'Pending Review'
        APPROVED = 'approved', 'Approved'
        REJECTED = 'rejected', 'Rejected'
        ARCHIVED = 'archived', 'Archived'

    creator = models.ForeignKey('creators.CreatorProfile', on_delete=models.CASCADE, related_name='reels')
    category = models.ForeignKey('content.Category', on_delete=models.SET_NULL, related_name='reels', null=True, blank=True)
    title = models.CharField(max_length=160)
    caption = models.TextField(blank=True)
    video_url = models.URLField(blank=True)
    hls_manifest_url = models.URLField(blank=True)
    thumbnail_url = models.URLField(blank=True)
    video_file = models.FileField(upload_to='reels/source/', null=True, blank=True)
    thumbnail_file = models.ImageField(upload_to='reels/thumbnails/', null=True, blank=True)
    duration_seconds = models.PositiveIntegerField(default=0)
    is_shareable = models.BooleanField(default=True)
    status = models.CharField(max_length=30, choices=Status.choices, default=Status.DRAFT)
    published_at = models.DateTimeField(null=True, blank=True)
    total_views = models.PositiveIntegerField(default=0)
    total_watch_seconds = models.PositiveBigIntegerField(default=0)
    total_likes = models.PositiveIntegerField(default=0)
    total_comments = models.PositiveIntegerField(default=0)
    total_votes = models.PositiveIntegerField(default=0)
    total_awards = models.PositiveIntegerField(default=0)
    total_shares = models.PositiveIntegerField(default=0)
    completion_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    recommendation_score = models.DecimalField(max_digits=12, decimal_places=4, default=0)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', 'created_at']),
            models.Index(fields=['status', 'recommendation_score']),
            models.Index(fields=['creator', 'status']),
        ]

    @property
    def thumbnail(self):
        if self.thumbnail_file:
            return self.thumbnail_file.url
        return self.thumbnail_url

    @property
    def stream_url(self):
        return self.hls_manifest_url or self.video_url or (self.video_file.url if self.video_file else '')

    def __str__(self):
        return self.title
