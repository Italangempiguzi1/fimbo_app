from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import WatchlistItem
from .serializers import WatchlistItemSerializer


class WatchlistAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        qs = WatchlistItem.objects.filter(user=request.user).select_related('content', 'content__creator', 'content__category')
        return Response(WatchlistItemSerializer(qs, many=True, context={'request': request}).data)

    def post(self, request):
        content_id = request.data.get('content') or request.data.get('content_id')
        obj, created = WatchlistItem.objects.get_or_create(user=request.user, content_id=content_id)
        if not created:
            obj.delete()
            return Response({'in_watchlist': False})
        return Response({'in_watchlist': True, 'item': WatchlistItemSerializer(obj, context={'request': request}).data}, status=201)
