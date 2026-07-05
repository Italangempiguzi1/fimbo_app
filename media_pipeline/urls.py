from rest_framework.routers import DefaultRouter
from .views import MediaJobViewSet
router = DefaultRouter()
router.register('jobs', MediaJobViewSet, basename='media-jobs')
urlpatterns = router.urls
