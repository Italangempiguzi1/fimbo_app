from django.urls import path
from .views import WatchEndAPIView, WatchHeartbeatAPIView, WatchStartAPIView

urlpatterns = [
    path('watch/start/', WatchStartAPIView.as_view(), name='watch-start'),
    path('watch/heartbeat/', WatchHeartbeatAPIView.as_view(), name='watch-heartbeat'),
    path('watch/end/', WatchEndAPIView.as_view(), name='watch-end'),
]
