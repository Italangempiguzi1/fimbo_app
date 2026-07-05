from django.db import models
from core.models import TimeStampedUUIDModel


class MediaJob(TimeStampedUUIDModel):
    class JobType(models.TextChoices):
        CONTENT_TRANSCODE = 'content_transcode', 'Content Transcode'
        REEL_TRANSCODE = 'reel_transcode', 'Reel Transcode'
        THUMBNAIL = 'thumbnail', 'Thumbnail'

    class Status(models.TextChoices):
        QUEUED = 'queued', 'Queued'
        PROCESSING = 'processing', 'Processing'
        DONE = 'done', 'Done'
        FAILED = 'failed', 'Failed'

    job_type = models.CharField(max_length=40, choices=JobType.choices)
    content = models.ForeignKey('content.Content', null=True, blank=True, on_delete=models.CASCADE)
    reel = models.ForeignKey('reels.Reel', null=True, blank=True, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.QUEUED)
    source_path = models.CharField(max_length=500, blank=True)
    output_hls_url = models.URLField(blank=True)
    output_mp4_url = models.URLField(blank=True)
    error_message = models.TextField(blank=True)

    class Meta:
        ordering = ['-created_at']
