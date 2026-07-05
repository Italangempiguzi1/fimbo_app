from rest_framework import generics, permissions
from .models import Report
from .serializers import ReportSerializer


class ReportCreateAPIView(generics.CreateAPIView):
    serializer_class = ReportSerializer
    permission_classes = [permissions.IsAuthenticated]


class MyReportsListAPIView(generics.ListAPIView):
    serializer_class = ReportSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Report.objects.filter(reporter=self.request.user)
