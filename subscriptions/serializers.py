from rest_framework import serializers
from .models import Plan, Subscription


class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = (
            'id', 'code', 'name', 'description', 'price_tzs', 'max_devices',
            'max_quality', 'downloads_enabled', 'early_access_enabled',
            'monthly_award_points', 'is_active'
        )
        read_only_fields = fields


class SubscriptionSerializer(serializers.ModelSerializer):
    plan = PlanSerializer(read_only=True)
    is_active_now = serializers.BooleanField(read_only=True)

    class Meta:
        model = Subscription
        fields = (
            'id', 'plan', 'status', 'started_at', 'expires_at', 'auto_renew',
            'provider_reference', 'is_active_now'
        )
        read_only_fields = fields


class DevActivateSubscriptionSerializer(serializers.Serializer):
    plan_code = serializers.SlugField()

    def validate_plan_code(self, value):
        if not Plan.objects.filter(code=value, is_active=True).exists():
            raise serializers.ValidationError('Unknown or inactive plan.')
        return value
