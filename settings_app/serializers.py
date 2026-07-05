from rest_framework import serializers
from .models import UserPreference

class UserPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPreference
        fields = '__all__'
        read_only_fields = ('id', 'user', 'created_at', 'updated_at')
