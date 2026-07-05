from django.conf import settings
from django.db import models
from core.models import TimeStampedUUIDModel


class CreatorProfile(TimeStampedUUIDModel):
    class VerificationStatus(models.TextChoices):
        PENDING = 'pending', 'Pending'
        VERIFIED = 'verified', 'Verified'
        REJECTED = 'rejected', 'Rejected'
        SUSPENDED = 'suspended', 'Suspended'

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='creator_profile')
    display_name = models.CharField(max_length=150)
    bio = models.TextField(blank=True)
    profile_image_url = models.URLField(blank=True)
    cover_image_url = models.URLField(blank=True)
    business_name = models.CharField(max_length=180, blank=True)
    content_focus = models.CharField(max_length=220, blank=True)
    verification_status = models.CharField(
        max_length=20,
        choices=VerificationStatus.choices,
        default=VerificationStatus.PENDING,
    )
    payout_phone = models.CharField(max_length=30, blank=True)
    bank_name = models.CharField(max_length=120, blank=True)
    bank_account_name = models.CharField(max_length=150, blank=True)
    bank_account_number = models.CharField(max_length=80, blank=True)
    total_followers = models.PositiveIntegerField(default=0)
    total_views = models.PositiveBigIntegerField(default=0)
    total_likes = models.PositiveBigIntegerField(default=0)
    total_votes = models.PositiveBigIntegerField(default=0)
    total_awards = models.PositiveBigIntegerField(default=0)
    total_watch_seconds = models.PositiveBigIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['display_name']

    def __str__(self):
        return self.display_name

    @property
    def is_verified(self):
        return self.is_active and self.verification_status == self.VerificationStatus.VERIFIED

    @property
    def can_upload(self):
        return self.is_active and self.verification_status == self.VerificationStatus.VERIFIED
