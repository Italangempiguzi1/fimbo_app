from django.utils import timezone
from rest_framework import permissions, viewsets
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from .models import BrandPlacement
from .serializers import BrandPlacementSerializer


class BrandPlacementViewSet(viewsets.ModelViewSet):
    serializer_class = BrandPlacementSerializer
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get_queryset(self):
        qs = BrandPlacement.objects.all()
        if self.request.user.is_authenticated and self.request.user.is_staff:
            return qs
        now = timezone.now()
        return qs.filter(is_active=True).filter(starts_at__isnull=True) | qs.filter(is_active=True, starts_at__lte=now, ends_at__isnull=True) | qs.filter(is_active=True, starts_at__lte=now, ends_at__gte=now)

    def get_permissions(self):
        if self.action in {'list', 'retrieve'}:
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]
