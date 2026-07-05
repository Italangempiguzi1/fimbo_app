from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, ContentViewSet

router = DefaultRouter()
router.register('categories', CategoryViewSet, basename='category')
router.register('items', ContentViewSet, basename='content')

urlpatterns = router.urls
