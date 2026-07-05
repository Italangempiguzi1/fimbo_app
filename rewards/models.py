from decimal import Decimal
from django.db import models
from core.models import TimeStampedUUIDModel


class RewardConfig(TimeStampedUUIDModel):
    name = models.CharField(max_length=120, default='Default reward formula')
    platform_share_percent = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('30.00'))
    creator_pool_percent = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('70.00'))
    watch_time_weight = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('40.00'))
    valid_views_weight = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('25.00'))
    engagement_weight = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('15.00'))
    votes_weight = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('10.00'))
    awards_weight = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('10.00'))
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class CreatorEarning(TimeStampedUUIDModel):
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        APPROVED = 'approved', 'Approved'
        PAID = 'paid', 'Paid'
        HELD = 'held', 'Held'

    creator = models.ForeignKey('creators.CreatorProfile', on_delete=models.CASCADE, related_name='earnings')
    period_start = models.DateField()
    period_end = models.DateField()
    gross_revenue_pool_tzs = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    creator_score = models.DecimalField(max_digits=12, decimal_places=4, default=0)
    amount_tzs = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    calculation_notes = models.TextField(blank=True)

    class Meta:
        unique_together = ('creator', 'period_start', 'period_end')
        ordering = ['-period_start']

    def __str__(self):
        return f'{self.creator} - {self.amount_tzs} TZS'


class Payout(TimeStampedUUIDModel):
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        PROCESSING = 'processing', 'Processing'
        PAID = 'paid', 'Paid'
        FAILED = 'failed', 'Failed'

    creator = models.ForeignKey('creators.CreatorProfile', on_delete=models.CASCADE, related_name='payouts')
    earning = models.ForeignKey(CreatorEarning, on_delete=models.PROTECT, related_name='payouts')
    amount_tzs = models.DecimalField(max_digits=14, decimal_places=2)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    payout_reference = models.CharField(max_length=150, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.creator} - {self.amount_tzs} - {self.status}'
