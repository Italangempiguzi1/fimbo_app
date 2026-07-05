import uuid
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from core.models import TimeStampedUUIDModel


class TargetType(models.TextChoices):
    CONTENT = 'content', 'Content'
    REEL = 'reel', 'Reel'


class Follow(TimeStampedUUIDModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='follows')
    creator = models.ForeignKey('creators.CreatorProfile', on_delete=models.CASCADE, related_name='followers')

    class Meta:
        unique_together = ('user', 'creator')
        ordering = ['-created_at']


class Like(TimeStampedUUIDModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='likes')
    target_type = models.CharField(max_length=20, choices=TargetType.choices)
    target_id = models.UUIDField(default=uuid.uuid4)

    class Meta:
        unique_together = ('user', 'target_type', 'target_id')
        ordering = ['-created_at']


class Vote(TimeStampedUUIDModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='votes')
    target_type = models.CharField(max_length=20, choices=TargetType.choices)
    target_id = models.UUIDField(default=uuid.uuid4)
    score = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

    class Meta:
        unique_together = ('user', 'target_type', 'target_id')
        ordering = ['-created_at']


class Comment(TimeStampedUUIDModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    target_type = models.CharField(max_length=20, choices=TargetType.choices)
    target_id = models.UUIDField(default=uuid.uuid4)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='replies', null=True, blank=True)
    text = models.TextField()
    is_hidden = models.BooleanField(default=False)
    is_pinned = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['target_type', 'target_id', 'created_at']),
            models.Index(fields=['parent', 'created_at']),
        ]


class Award(TimeStampedUUIDModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='awards_given')
    creator = models.ForeignKey('creators.CreatorProfile', on_delete=models.CASCADE, related_name='awards_received')
    target_type = models.CharField(max_length=20, choices=TargetType.choices)
    target_id = models.UUIDField(default=uuid.uuid4)
    points = models.PositiveIntegerField(default=1)
    message = models.CharField(max_length=240, blank=True)

    class Meta:
        ordering = ['-created_at']
