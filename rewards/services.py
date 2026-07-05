from decimal import Decimal
from django.db.models import Sum
from analytics.models import WatchSession
from creators.models import CreatorProfile
from .models import CreatorEarning


def calculate_creator_rewards(period_start, period_end, gross_revenue_pool_tzs):
    """Simple MVP formula. Add anti-fraud checks before real production payouts."""
    sessions = WatchSession.objects.filter(started_at__date__gte=period_start, started_at__date__lte=period_end)
    totals = sessions.aggregate(total_watch_seconds=Sum('seconds_watched'))
    total_watch_seconds = totals.get('total_watch_seconds') or 0
    if total_watch_seconds == 0:
        return []

    created = []
    for creator in CreatorProfile.objects.filter(is_active=True):
        creator_watch_seconds = sessions.filter(creator=creator).aggregate(total=Sum('seconds_watched')).get('total') or 0
        if creator_watch_seconds == 0:
            continue
        score = Decimal(creator_watch_seconds) / Decimal(total_watch_seconds)
        amount = Decimal(gross_revenue_pool_tzs) * score
        earning, _ = CreatorEarning.objects.update_or_create(
            creator=creator,
            period_start=period_start,
            period_end=period_end,
            defaults={
                'gross_revenue_pool_tzs': gross_revenue_pool_tzs,
                'creator_score': score,
                'amount_tzs': amount,
                'calculation_notes': 'MVP formula: share of total watch seconds.',
            },
        )
        created.append(earning)
    return created
