from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

class RecommendationExplainAPIView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        return Response({
            'content_algorithm': ['watch_time', 'views', 'likes', 'comments', 'votes', 'awards', 'freshness'],
            'reels_algorithm': ['watch_time', 'completion_rate', 'likes', 'comments', 'votes', 'awards', 'shares', 'freshness'],
            'note': 'MVP ranking uses transparent weighted signals and can later be replaced by ML recommendations.'
        })
