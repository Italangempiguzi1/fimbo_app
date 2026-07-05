from rest_framework import generics, permissions
from .models import CreatorEarning, Payout
from .serializers import CreatorEarningSerializer, PayoutSerializer


class MyEarningsListAPIView(generics.ListAPIView):
    serializer_class = CreatorEarningSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        profile = getattr(self.request.user, 'creator_profile', None)
        if not profile:
            return CreatorEarning.objects.none()
        return CreatorEarning.objects.filter(creator=profile)


class MyPayoutsListAPIView(generics.ListAPIView):
    serializer_class = PayoutSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        profile = getattr(self.request.user, 'creator_profile', None)
        if not profile:
            return Payout.objects.none()
        return Payout.objects.filter(creator=profile)
