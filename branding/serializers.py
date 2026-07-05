from rest_framework import serializers
from .models import BrandPlacement


class BrandPlacementSerializer(serializers.ModelSerializer):
    image = serializers.CharField(read_only=True)

    class Meta:
        model = BrandPlacement
        fields = '__all__'
