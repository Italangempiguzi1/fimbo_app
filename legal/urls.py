from rest_framework.routers import DefaultRouter
from .views import HelpArticleViewSet, LegalPageViewSet
router = DefaultRouter()
router.register('pages', LegalPageViewSet, basename='legal-pages')
router.register('help', HelpArticleViewSet, basename='help')
urlpatterns = router.urls
