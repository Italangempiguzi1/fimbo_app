from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import CurrentSubscriptionAPIView, DevActivateSubscriptionAPIView, PlanViewSet

router = DefaultRouter()
router.register('plans', PlanViewSet, basename='plan')

urlpatterns = [
    path('current/', CurrentSubscriptionAPIView.as_view(), name='current-subscription'),
    path('activate-dev/', DevActivateSubscriptionAPIView.as_view(), name='activate-dev-subscription'),
]
urlpatterns += router.urls
