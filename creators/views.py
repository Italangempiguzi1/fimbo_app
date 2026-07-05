from django.db.models import Sum
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from engagement.models import Award, Follow, Like, TargetType, Vote
from analytics.models import WatchSession
from content.models import Content
from reels.models import Reel
from .models import CreatorProfile
from .serializers import CreatorProfileSerializer


class MyCreatorProfileAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        profile = getattr(request.user, 'creator_profile', None)
        if not profile:
            return Response({'detail': 'No creator profile found.'}, status=404)
        return Response(CreatorProfileSerializer(profile).data)

    def post(self, request):
        profile, _ = CreatorProfile.objects.get_or_create(
            user=request.user,
            defaults={
                'display_name': request.data.get('display_name') or request.user.get_full_name() or request.user.username,
                'verification_status': CreatorProfile.VerificationStatus.PENDING,
            },
        )
        serializer = CreatorProfileSerializer(profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class CreatorDashboardAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        profile = getattr(request.user, 'creator_profile', None)
        if not profile:
            return Response({'detail': 'No creator profile found.'}, status=404)
        content_qs = Content.objects.filter(creator=profile)
        reels_qs = Reel.objects.filter(creator=profile)
        content_ids = list(content_qs.values_list('id', flat=True))
        reel_ids = list(reels_qs.values_list('id', flat=True))
        watch_seconds = WatchSession.objects.filter(creator=profile, is_valid_view=True).aggregate(total=Sum('seconds_watched'))['total'] or 0
        total_views = (content_qs.aggregate(total=Sum('total_views'))['total'] or 0) + (reels_qs.aggregate(total=Sum('total_views'))['total'] or 0)
        totals = {
            'content_posted': content_qs.count(),
            'reels_posted': reels_qs.count(),
            'followers': Follow.objects.filter(creator=profile).count(),
            'views': total_views,
            'likes': Like.objects.filter(target_type=TargetType.CONTENT, target_id__in=content_ids).count() + Like.objects.filter(target_type=TargetType.REEL, target_id__in=reel_ids).count(),
            'votes': Vote.objects.filter(target_type=TargetType.CONTENT, target_id__in=content_ids).count() + Vote.objects.filter(target_type=TargetType.REEL, target_id__in=reel_ids).count(),
            'awards': Award.objects.filter(creator=profile).count(),
            'watch_seconds': watch_seconds,
        }
        return Response({
            'profile': CreatorProfileSerializer(profile).data,
            'totals': totals,
            'recent_content': list(content_qs.order_by('-created_at').values('id', 'title', 'status', 'total_views', 'total_watch_seconds')[:8]),
            'recent_reels': list(reels_qs.order_by('-created_at').values('id', 'title', 'status', 'total_views', 'total_watch_seconds')[:8]),
        })


class PublicCreatorProfileAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, pk):
        try:
            profile = CreatorProfile.objects.get(pk=pk, is_active=True)
        except CreatorProfile.DoesNotExist:
            return Response({'detail': 'Creator not found.'}, status=404)
        return Response(CreatorProfileSerializer(profile).data)
