from rest_framework import serializers
from subscriptions.models import Plan
from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = (
            'id', 'plan', 'subscription', 'provider', 'status', 'amount', 'currency',
            'phone', 'provider_reference', 'checkout_url', 'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'subscription', 'status', 'amount', 'currency', 'provider_reference', 'checkout_url', 'created_at', 'updated_at')


class PaymentInitiateSerializer(serializers.Serializer):
    plan_code = serializers.SlugField()
    provider = serializers.ChoiceField(choices=Payment.Provider.choices)
    phone = serializers.CharField(max_length=30, required=False, allow_blank=True)

    def validate_plan_code(self, value):
        try:
            return Plan.objects.get(code=value, is_active=True)
        except Plan.DoesNotExist as exc:
            raise serializers.ValidationError('Unknown or inactive plan.') from exc
