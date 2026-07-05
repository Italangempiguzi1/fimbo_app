from rest_framework import serializers
from .models import WatchSession


class WatchStartSerializer(serializers.Serializer):
    target_type = serializers.ChoiceField(choices=(('content', 'Content'), ('reel', 'Reel')))
    target_id = serializers.UUIDField()
    device_id = serializers.CharField(required=False, allow_blank=True)


class WatchHeartbeatSerializer(serializers.Serializer):
    watch_session_id = serializers.UUIDField()
    seconds_watched = serializers.IntegerField(min_value=0)
    playback_position_seconds = serializers.IntegerField(min_value=0, required=False, default=0)


class WatchEndSerializer(serializers.Serializer):
    watch_session_id = serializers.UUIDField()
    seconds_watched = serializers.IntegerField(min_value=0)
    completed = serializers.BooleanField(default=False)


class WatchSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = WatchSession
        fields = '__all__'
        read_only_fields = ('id', 'user', 'creator', 'started_at', 'ended_at', 'is_valid_view', 'created_at', 'updated_at')
