from datetime import timedelta
from django.utils import timezone
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from subscriptions.services import has_active_subscription
from .models import DownloadLicense
from .serializers import DownloadLicenseSerializer


class DownloadLicenseListCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        qs = DownloadLicense.objects.filter(user=request.user).select_related('content')
        return Response(DownloadLicenseSerializer(qs, many=True, context={'request': request}).data)

    def post(self, request):
        if not has_active_subscription(request.user):
            return Response({'detail': 'Active subscription required.', 'code': 'subscription_required'}, status=status.HTTP_402_PAYMENT_REQUIRED)
        content_id = request.data.get('content') or request.data.get('content_id')
        license_obj, _ = DownloadLicense.objects.update_or_create(
            user=request.user,
            content_id=content_id,
            defaults={'expires_at': timezone.now() + timedelta(days=30), 'status': DownloadLicense.Status.ACTIVE}
        )
        return Response(DownloadLicenseSerializer(license_obj, context={'request': request}).data, status=201)
