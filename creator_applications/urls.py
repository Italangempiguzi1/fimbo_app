from django.urls import path
from .views import CreatorApplicationReviewAPIView, MyCreatorApplicationAPIView

urlpatterns = [
    path('me/', MyCreatorApplicationAPIView.as_view(), name='my-creator-application'),
    path('<uuid:pk>/review/', CreatorApplicationReviewAPIView.as_view(), name='review-creator-application'),
]
