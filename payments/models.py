from django.conf import settings
from django.db import models
from core.models import TimeStampedUUIDModel


class Payment(TimeStampedUUIDModel):
    class Provider(models.TextChoices):
        MOBILE_MONEY = 'mobile_money', 'Mobile Money'
        CARD = 'card', 'Card'
        BANK = 'bank', 'Bank'
        INTERNAL = 'internal', 'Internal'

    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        SUCCESS = 'success', 'Success'
        FAILED = 'failed', 'Failed'
        CANCELLED = 'cancelled', 'Cancelled'
        REFUNDED = 'refunded', 'Refunded'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='payments')
    plan = models.ForeignKey('subscriptions.Plan', on_delete=models.PROTECT, related_name='payments', null=True, blank=True)
    subscription = models.ForeignKey('subscriptions.Subscription', on_delete=models.SET_NULL, related_name='payments', null=True, blank=True)
    provider = models.CharField(max_length=30, choices=Provider.choices)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=10, default='TZS')
    phone = models.CharField(max_length=30, blank=True)
    provider_reference = models.CharField(max_length=150, blank=True)
    checkout_url = models.URLField(blank=True)
    raw_payload = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [models.Index(fields=['user', 'status', 'created_at'])]

    def __str__(self):
        return f'{self.user} - {self.amount} {self.currency} - {self.status}'
