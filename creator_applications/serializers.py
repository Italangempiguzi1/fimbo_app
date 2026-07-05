from rest_framework import serializers
from .models import CreatorApplication


class CreatorApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreatorApplication
        fields = '__all__'
        read_only_fields = ('id', 'user', 'status', 'review_note', 'created_at', 'updated_at')


class CreatorApplicationReviewSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=[('approved', 'Approved'), ('rejected', 'Rejected')])
    review_note = serializers.CharField(required=False, allow_blank=True)
