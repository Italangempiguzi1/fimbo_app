from django.db.models import Count
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Award, Comment, Follow, Like, Vote
from .serializers import AwardSerializer, CommentSerializer, FollowSerializer, LikeSerializer, VoteSerializer
from .services import get_target_creator, get_target_or_404, increment_counter


class ToggleLikeAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = LikeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        target = get_target_or_404(data['target_type'], data['target_id'])
        obj, created = Like.objects.get_or_create(user=request.user, **data)
        if not created:
            obj.delete()
            increment_counter(target, 'total_likes', -1)
            return Response({'liked': False})
        increment_counter(target, 'total_likes', 1)
        return Response({'liked': True})


class VoteAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = VoteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        target = get_target_or_404(data['target_type'], data['target_id'])
        _, created = Vote.objects.update_or_create(
            user=request.user, target_type=data['target_type'], target_id=data['target_id'], defaults={'score': data['score']}
        )
        if created:
            increment_counter(target, 'total_votes', 1)
        return Response({'voted': True, 'score': data['score']})


class ToggleFollowAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = FollowSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        creator_id = serializer.validated_data['creator_id']
        obj, created = Follow.objects.get_or_create(user=request.user, creator_id=creator_id)
        if not created:
            obj.delete()
            return Response({'following': False})
        return Response({'following': True})


class CommentListCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        target_type = request.query_params.get('target_type')
        target_id = request.query_params.get('target_id')
        parent = request.query_params.get('parent')
        qs = Comment.objects.filter(is_hidden=False).annotate(replies_count=Count('replies'))
        if target_type and target_id:
            qs = qs.filter(target_type=target_type, target_id=target_id)
        if parent:
            qs = qs.filter(parent_id=parent)
        else:
            qs = qs.filter(parent__isnull=True)
        qs = qs.order_by('-is_pinned', '-created_at')
        serializer = CommentSerializer(qs[:100], many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        target = get_target_or_404(serializer.validated_data['target_type'], serializer.validated_data['target_id'])
        comment = serializer.save(user=request.user)
        if not comment.parent_id:
            increment_counter(target, 'total_comments', 1)
        return Response(CommentSerializer(comment).data, status=201)


class AwardAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = AwardSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        creator = get_target_creator(serializer.validated_data['target_type'], serializer.validated_data['target_id'])
        target = get_target_or_404(serializer.validated_data['target_type'], serializer.validated_data['target_id'])
        award = serializer.save(user=request.user, creator=creator)
        increment_counter(target, 'total_awards', 1)
        return Response(AwardSerializer(award).data, status=201)
