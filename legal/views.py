from rest_framework import permissions, viewsets
from .models import HelpArticle, LegalPage
from .serializers import HelpArticleSerializer, LegalPageSerializer

class LegalPageViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = LegalPage.objects.filter(is_published=True)
    serializer_class = LegalPageSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'slug'

class HelpArticleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = HelpArticle.objects.filter(is_published=True)
    serializer_class = HelpArticleSerializer
    permission_classes = [permissions.AllowAny]
