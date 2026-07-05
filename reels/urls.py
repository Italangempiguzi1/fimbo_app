from rest_framework.routers import DefaultRouter
from .views import ReelViewSet

router = DefaultRouter()
router.register('', ReelViewSet, basename='reel')

urlpatterns = router.urls
