from django.urls import path
from .views import MyPaymentListAPIView, PaymentInitiateAPIView

urlpatterns = [
    path('', MyPaymentListAPIView.as_view(), name='my-payments'),
    path('initiate/', PaymentInitiateAPIView.as_view(), name='payment-initiate'),
]
