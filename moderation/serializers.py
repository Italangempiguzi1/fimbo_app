from rest_framework import serializers
from engagement.services import get_target_or_404
from .models import Report


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ('id', 'target_type', 'target_id', 'reason', 'description', 'status', 'created_at')
        read_only_fields = ('id', 'status', 'created_at')

    def validate(self, attrs):
        get_target_or_404(attrs['target_type'], attrs['target_id'])
        return attrs

    def create(self, validated_data):
        return Report.objects.create(reporter=self.context['request'].user, **validated_data)
