from rest_framework import serializers
from .models import CreatorEarning, Payout


class CreatorEarningSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreatorEarning
        fields = (
            'id', 'period_start', 'period_end', 'gross_revenue_pool_tzs',
            'creator_score', 'amount_tzs', 'status', 'calculation_notes', 'created_at'
        )
        read_only_fields = fields


class PayoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payout
        fields = ('id', 'earning', 'amount_tzs', 'status', 'payout_reference', 'notes', 'created_at')
        read_only_fields = fields
