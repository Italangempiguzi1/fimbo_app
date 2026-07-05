from django.urls import path
from .views import CreatorDashboardAPIView, MyCreatorProfileAPIView, PublicCreatorProfileAPIView

urlpatterns = [
    path('me/', MyCreatorProfileAPIView.as_view(), name='my-creator-profile'),
    path('dashboard/', CreatorDashboardAPIView.as_view(), name='creator-dashboard'),
    path('<uuid:pk>/', PublicCreatorProfileAPIView.as_view(), name='creator-public-detail'),
]
