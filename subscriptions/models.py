from datetime import timedelta
from django.conf import settings
from django.db import models
from django.utils import timezone
from core.models import TimeStampedUUIDModel


class Plan(TimeStampedUUIDModel):
    code = models.SlugField(unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price_tzs = models.DecimalField(max_digits=12, decimal_places=2)
    max_devices = models.PositiveSmallIntegerField(default=1)
    max_quality = models.CharField(max_length=20, default='720p')
    downloads_enabled = models.BooleanField(default=False)
    early_access_enabled = models.BooleanField(default=False)
    monthly_award_points = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['price_tzs']

    def __str__(self):
        return f'{self.name} - TZS {self.price_tzs}'


class Subscription(TimeStampedUUIDModel):
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        ACTIVE = 'active', 'Active'
        EXPIRED = 'expired', 'Expired'
        CANCELLED = 'cancelled', 'Cancelled'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='subscriptions')
    plan = models.ForeignKey(Plan, on_delete=models.PROTECT, related_name='subscriptions')
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    started_at = models.DateTimeField(default=timezone.now)
    expires_at = models.DateTimeField()
    auto_renew = models.BooleanField(default=False)
    provider_reference = models.CharField(max_length=150, blank=True)

    class Meta:
        ordering = ['-expires_at']
        indexes = [
            models.Index(fields=['user', 'status', 'expires_at']),
        ]

    def __str__(self):
        return f'{self.user} - {self.plan} - {self.status}'

    @property
    def is_active_now(self):
        return self.status == self.Status.ACTIVE and self.expires_at > timezone.now()

    @classmethod
    def create_monthly(cls, user, plan, provider_reference=''):
        now = timezone.now()
        return cls.objects.create(
            user=user,
            plan=plan,
            status=cls.Status.ACTIVE,
            started_at=now,
            expires_at=now + timedelta(days=30),
            provider_reference=provider_reference,
        )
