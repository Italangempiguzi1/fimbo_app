from rest_framework import permissions, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Plan, Subscription
from .serializers import DevActivateSubscriptionSerializer, PlanSerializer, SubscriptionSerializer
from .services import get_active_subscription


class PlanViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Plan.objects.filter(is_active=True)
    serializer_class = PlanSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'code'


class CurrentSubscriptionAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        subscription = get_active_subscription(request.user)
        if not subscription:
            return Response({'active': False, 'subscription': None})
        return Response({'active': True, 'subscription': SubscriptionSerializer(subscription).data})


class DevActivateSubscriptionAPIView(APIView):
    """MVP-only endpoint for local testing. Remove or protect before production."""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = DevActivateSubscriptionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        plan = Plan.objects.get(code=serializer.validated_data['plan_code'], is_active=True)
        subscription = Subscription.create_monthly(
            user=request.user,
            plan=plan,
            provider_reference='DEV-ACTIVATION',
        )
        return Response(SubscriptionSerializer(subscription).data, status=201)
