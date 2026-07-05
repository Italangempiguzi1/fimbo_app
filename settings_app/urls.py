from django.urls import path
from .views import MyPreferenceAPIView
urlpatterns = [path('me/', MyPreferenceAPIView.as_view(), name='my-preferences')]
