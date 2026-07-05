from rest_framework import serializers
from .models import MediaJob

class MediaJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaJob
        fields = '__all__'
