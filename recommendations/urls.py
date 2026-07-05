from django.urls import path
from .views import RecommendationExplainAPIView
urlpatterns = [path('explain/', RecommendationExplainAPIView.as_view(), name='recommendation-explain')]
