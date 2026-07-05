from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from subscriptions.services import has_active_subscription
from engagement.services import get_target_creator, get_target_or_404
from .models import WatchSession
from .serializers import WatchEndSerializer, WatchHeartbeatSerializer, WatchSessionSerializer, WatchStartSerializer


def get_client_ip(request):
    forwarded = request.META.get('HTTP_X_FORWARDED_FOR')
    if forwarded:
        return forwarded.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR')


class WatchStartAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        if not has_active_subscription(request.user):
            return Response({'detail': 'Active subscription required.', 'code': 'subscription_required'}, status=status.HTTP_402_PAYMENT_REQUIRED)
        serializer = WatchStartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        creator = get_target_creator(data['target_type'], data['target_id'])
        session = WatchSession.objects.create(
            user=request.user,
            creator=creator,
            target_type=data['target_type'],
            target_id=data['target_id'],
            device_id=data.get('device_id', ''),
            ip_address=get_client_ip(request),
        )
        return Response(WatchSessionSerializer(session).data, status=201)


class WatchHeartbeatAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = WatchHeartbeatSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        session = get_object_or_404(WatchSession, id=serializer.validated_data['watch_session_id'], user=request.user)
        session.seconds_watched = max(session.seconds_watched, serializer.validated_data['seconds_watched'])
        session.save(update_fields=['seconds_watched', 'updated_at'])
        return Response(WatchSessionSerializer(session).data)


class WatchEndAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @transaction.atomic
    def post(self, request):
        serializer = WatchEndSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        session = get_object_or_404(
            WatchSession.objects.select_for_update(),
            id=serializer.validated_data['watch_session_id'],
            user=request.user,
        )
        seconds = serializer.validated_data['seconds_watched']
        completed = serializer.validated_data['completed']
        target = get_target_or_404(session.target_type, session.target_id)
        threshold = 3 if session.target_type == 'reel' else 30
        session.ended_at = session.ended_at or None
        session.mark_ended(seconds_watched=seconds, completed=completed)
        session.is_valid_view = seconds >= threshold or completed
        session.save(update_fields=['is_valid_view', 'updated_at'])
        target.total_watch_seconds = target.total_watch_seconds + seconds
        if session.is_valid_view:
            target.total_views = target.total_views + 1
        target.save(update_fields=['total_watch_seconds', 'total_views', 'updated_at'])
        return Response(WatchSessionSerializer(session).data)
