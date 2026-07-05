from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import UserPreference
from .serializers import UserPreferenceSerializer

class MyPreferenceAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        prefs, _ = UserPreference.objects.get_or_create(user=request.user)
        return Response(UserPreferenceSerializer(prefs).data)
    def patch(self, request):
        prefs, _ = UserPreference.objects.get_or_create(user=request.user)
        serializer = UserPreferenceSerializer(prefs, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
