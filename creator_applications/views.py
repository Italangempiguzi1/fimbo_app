from rest_framework import permissions, status
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView
from creators.models import CreatorProfile
from users.models import User
from .models import CreatorApplication
from .serializers import CreatorApplicationReviewSerializer, CreatorApplicationSerializer


class MyCreatorApplicationAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get(self, request):
        app = getattr(request.user, 'creator_application', None)
        if not app:
            return Response({'detail': 'No creator application found.'}, status=404)
        return Response(CreatorApplicationSerializer(app).data)

    def post(self, request):
        app, _ = CreatorApplication.objects.update_or_create(
            user=request.user,
            defaults={**request.data, 'status': CreatorApplication.Status.SUBMITTED}
        )
        serializer = CreatorApplicationSerializer(app)
        return Response(serializer.data, status=201)


class CreatorApplicationReviewAPIView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def post(self, request, pk):
        serializer = CreatorApplicationReviewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        app = CreatorApplication.objects.get(pk=pk)
        app.status = serializer.validated_data['status']
        app.review_note = serializer.validated_data.get('review_note', '')
        app.save(update_fields=['status', 'review_note', 'updated_at'])
        if app.status == CreatorApplication.Status.APPROVED:
            CreatorProfile.objects.update_or_create(
                user=app.user,
                defaults={
                    'display_name': app.display_name,
                    'business_name': app.business_name,
                    'content_focus': app.content_type,
                    'verification_status': CreatorProfile.VerificationStatus.VERIFIED,
                }
            )
            app.user.role = User.Role.CREATOR
            app.user.save(update_fields=['role'])
        return Response(CreatorApplicationSerializer(app).data)
