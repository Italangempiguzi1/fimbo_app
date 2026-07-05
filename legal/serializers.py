from rest_framework import serializers
from .models import HelpArticle, LegalPage

class LegalPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = LegalPage
        fields = '__all__'

class HelpArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = HelpArticle
        fields = '__all__'
