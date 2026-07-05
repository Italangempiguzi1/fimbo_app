from django.urls import path
from .views import MyEarningsListAPIView, MyPayoutsListAPIView

urlpatterns = [
    path('earnings/', MyEarningsListAPIView.as_view(), name='my-earnings'),
    path('payouts/', MyPayoutsListAPIView.as_view(), name='my-payouts'),
]
