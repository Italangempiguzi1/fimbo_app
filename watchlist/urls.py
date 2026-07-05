from django.urls import path
from .views import WatchlistAPIView
urlpatterns = [path('', WatchlistAPIView.as_view(), name='watchlist')]
