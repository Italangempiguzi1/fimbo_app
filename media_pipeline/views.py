from rest_framework import permissions, viewsets
from .models import MediaJob
from .serializers import MediaJobSerializer

class MediaJobViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = MediaJob.objects.all()
    serializer_class = MediaJobSerializer
    permission_classes = [permissions.IsAdminUser]
