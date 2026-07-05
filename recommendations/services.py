# from django.db.models import F, FloatField, Value
# from django.db.models.functions import Coalesce


# def ranked_content_queryset(qs, user=None):
#     # Simple MVP ranking: combines engagement, watch time, quality, freshness flags.
#     return qs.annotate(
#         rank_score=(
#             Coalesce(F('recommendation_score'), Value(0.0, output_field=FloatField())) +
#             Coalesce(F('total_views'), Value(0)) * 2.0 +
#             Coalesce(F('total_watch_seconds'), Value(0)) * 0.002 +
#             Coalesce(F('total_likes'), Value(0)) * 3.0 +
#             Coalesce(F('total_comments'), Value(0)) * 4.0 +
#             Coalesce(F('total_votes'), Value(0)) * 3.5 +
#             Coalesce(F('total_awards'), Value(0)) * 5.0
#         )
#     ).order_by('-rank_score', '-published_at', '-created_at')


# def ranked_reels_queryset(qs, user=None):
#     # TikTok/Instagram-inspired lightweight feed: watch time + completion + engagement + shares + freshness.
#     return qs.annotate(
#         rank_score=(
#             Coalesce(F('recommendation_score'), Value(0.0, output_field=FloatField())) +
#             Coalesce(F('total_watch_seconds'), Value(0)) * 0.01 +
#             Coalesce(F('total_views'), Value(0)) * 1.5 +
#             Coalesce(F('total_likes'), Value(0)) * 3.0 +
#             Coalesce(F('total_comments'), Value(0)) * 4.0 +
#             Coalesce(F('total_votes'), Value(0)) * 2.0 +
#             Coalesce(F('total_awards'), Value(0)) * 5.0 +
#             Coalesce(F('total_shares'), Value(0)) * 4.0
#         )
#     ).order_by('-rank_score', '-published_at', '-created_at')

from decimal import Decimal

from django.db.models import (
    DecimalField,
    ExpressionWrapper,
    F,
    Value,
)
from django.db.models.functions import Coalesce


def ranked_content_queryset(qs, user=None):

    rank_score = ExpressionWrapper(

        Coalesce(
            F("recommendation_score"),
            Value(
                Decimal("0.0000"),
                output_field=DecimalField(max_digits=12, decimal_places=4),
            ),
        )

        + Coalesce(F("total_views"), Value(0))
            * Decimal("2.0")

        + Coalesce(F("total_watch_seconds"), Value(0))
            * Decimal("0.002")

        + Coalesce(F("total_likes"), Value(0))
            * Decimal("3.0")

        + Coalesce(F("total_comments"), Value(0))
            * Decimal("4.0")

        + Coalesce(F("total_votes"), Value(0))
            * Decimal("3.5")

        + Coalesce(F("total_awards"), Value(0))
            * Decimal("5.0"),

        output_field=DecimalField(
            max_digits=20,
            decimal_places=4,
        ),
    )

    return qs.annotate(
        rank_score=rank_score
    ).order_by(
        "-rank_score",
        "-published_at",
        "-created_at",
    )


def ranked_reels_queryset(qs, user=None):

    rank_score = ExpressionWrapper(

        Coalesce(
            F("recommendation_score"),
            Value(
                Decimal("0.0000"),
                output_field=DecimalField(max_digits=12, decimal_places=4),
            ),
        )

        + Coalesce(F("total_watch_seconds"), Value(0))
            * Decimal("0.01")

        + Coalesce(F("total_views"), Value(0))
            * Decimal("1.5")

        + Coalesce(F("total_likes"), Value(0))
            * Decimal("3.0")

        + Coalesce(F("total_comments"), Value(0))
            * Decimal("4.0")

        + Coalesce(F("total_votes"), Value(0))
            * Decimal("2.0")

        + Coalesce(F("total_awards"), Value(0))
            * Decimal("5.0")

        + Coalesce(F("total_shares"), Value(0))
            * Decimal("4.0"),

        output_field=DecimalField(
            max_digits=20,
            decimal_places=4,
        ),
    )

    return qs.annotate(
        rank_score=rank_score
    ).order_by(
        "-rank_score",
        "-published_at",
        "-created_at",
    )