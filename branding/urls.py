from rest_framework.routers import DefaultRouter
from .views import BrandPlacementViewSet

router = DefaultRouter()
router.register('', BrandPlacementViewSet, basename='branding')
urlpatterns = router.urls
