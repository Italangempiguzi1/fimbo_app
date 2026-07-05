from rest_framework import serializers
from .models import Award, Comment, Follow, Like, TargetType, Vote


class TargetActionSerializer(serializers.Serializer):
    target_type = serializers.ChoiceField(choices=TargetType.choices)
    target_id = serializers.UUIDField()


class LikeSerializer(TargetActionSerializer):
    pass


class VoteSerializer(TargetActionSerializer):
    score = serializers.IntegerField(min_value=1, max_value=5)


class FollowSerializer(serializers.Serializer):
    creator_id = serializers.UUIDField()


class CommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    avatar_url = serializers.CharField(source='user.avatar_url', read_only=True)
    replies_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'user', 'username', 'avatar_url', 'target_type', 'target_id', 'parent', 'text', 'is_hidden', 'is_pinned', 'replies_count', 'created_at', 'updated_at')
        read_only_fields = ('id', 'user', 'is_hidden', 'is_pinned', 'created_at', 'updated_at')


class AwardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Award
        fields = ('id', 'creator', 'target_type', 'target_id', 'points', 'message', 'created_at')
        read_only_fields = ('id', 'created_at')
