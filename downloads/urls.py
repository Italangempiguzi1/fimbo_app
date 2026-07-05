from django.urls import path
from .views import DownloadLicenseListCreateAPIView
urlpatterns = [path('', DownloadLicenseListCreateAPIView.as_view(), name='download-licenses')]
