from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Payment
from .serializers import PaymentInitiateSerializer, PaymentSerializer


class MyPaymentListAPIView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Payment.objects.filter(user=self.request.user)


class PaymentInitiateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = PaymentInitiateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        plan = serializer.validated_data['plan_code']
        payment = Payment.objects.create(
            user=request.user,
            plan=plan,
            provider=serializer.validated_data['provider'],
            amount=plan.price_tzs,
            currency='TZS',
            phone=serializer.validated_data.get('phone', ''),
            status=Payment.Status.PENDING,
        )
        return Response({
            'payment': PaymentSerializer(payment).data,
            'detail': 'Payment record created. Integrate provider checkout/callback here.',
        }, status=201)
