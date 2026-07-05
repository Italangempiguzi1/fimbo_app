from django.urls import path
from .views import MyReportsListAPIView, ReportCreateAPIView

urlpatterns = [
    path('reports/', MyReportsListAPIView.as_view(), name='my-reports'),
    path('reports/create/', ReportCreateAPIView.as_view(), name='report-create'),
]
