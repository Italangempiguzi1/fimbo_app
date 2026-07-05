from django.utils import timezone
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Notification
from .serializers import NotificationSerializer


class MyNotificationListAPIView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = Notification.objects.filter(user=self.request.user)
        is_read = self.request.query_params.get('is_read')
        if is_read in {'true', 'false'}:
            qs = qs.filter(is_read=(is_read == 'true'))
        return qs


class NotificationMarkReadAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        notification = Notification.objects.filter(id=pk, user=request.user).first()
        if not notification:
            return Response({'detail': 'Notification not found.'}, status=status.HTTP_404_NOT_FOUND)
        notification.is_read = True
        notification.read_at = timezone.now()
        notification.save(update_fields=['is_read', 'read_at', 'updated_at'])
        return Response(NotificationSerializer(notification).data)
