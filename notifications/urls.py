from django.urls import path
from .views import MyNotificationListAPIView, NotificationMarkReadAPIView

urlpatterns = [
    path('', MyNotificationListAPIView.as_view(), name='my-notifications'),
    path('<uuid:pk>/mark_read/', NotificationMarkReadAPIView.as_view(), name='notification-mark-read'),
]
