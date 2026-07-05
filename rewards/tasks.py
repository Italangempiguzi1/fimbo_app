from celery import shared_task
from django.utils import timezone
from .services import calculate_creator_rewards


@shared_task
def calculate_monthly_rewards(period_start_iso, period_end_iso, gross_revenue_pool_tzs):
    period_start = timezone.datetime.fromisoformat(period_start_iso).date()
    period_end = timezone.datetime.fromisoformat(period_end_iso).date()
    earnings = calculate_creator_rewards(period_start, period_end, gross_revenue_pool_tzs)
    return {'created_or_updated': len(earnings)}
