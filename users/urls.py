from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenBlacklistView
from .views import RegisterAPIView, MeAPIView

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('token/', TokenObtainPairView.as_view(), name='token-obtain-pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('token/logout/', TokenBlacklistView.as_view(), name='token-blacklist'),
    path('me/', MeAPIView.as_view(), name='me'),
]
