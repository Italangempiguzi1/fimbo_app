from django.utils import timezone
from .models import Subscription


def get_active_subscription(user):
    if not user or not user.is_authenticated:
        return None
    return (
        Subscription.objects
        .filter(user=user, status=Subscription.Status.ACTIVE, expires_at__gt=timezone.now())
        .select_related('plan')
        .order_by('-expires_at')
        .first()
    )


def has_active_subscription(user):
    return get_active_subscription(user) is not None
