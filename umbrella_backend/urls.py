from django.contrib import admin
from django.urls import include, path
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny


@api_view(['GET'])
@permission_classes([AllowAny])
def api_root(request):
    return Response({
        'name': 'Umbrella MVP Backend',
        'version': '0.1.0',
        'modules': [
            'auth', 'creators', 'subscriptions', 'payments', 'content', 'reels',
            'engagement', 'analytics', 'rewards', 'moderation', 'notifications', 'home', 'branding', 'creator_applications', 'downloads', 'legal', 'settings', 'media_pipeline', 'watchlist'
        ]
    })


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api_root, name='api-root'),
    path('api/auth/', include('users.urls')),
    path('api/creators/', include('creators.urls')),
    path('api/subscriptions/', include('subscriptions.urls')),
    path('api/payments/', include('payments.urls')),
    path('api/content/', include('content.urls')),
    path('api/reels/', include('reels.urls')),
    path('api/engagement/', include('engagement.urls')),
    path('api/analytics/', include('analytics.urls')),
    path('api/rewards/', include('rewards.urls')),
    path('api/moderation/', include('moderation.urls')),
    path('api/notifications/', include('notifications.urls')),
    path('api/home/', include('home.urls')),
    path('api/branding/', include('branding.urls')),
    path('api/creator-applications/', include('creator_applications.urls')),
    path('api/downloads/', include('downloads.urls')),
    path('api/legal/', include('legal.urls')),
    path('api/settings/', include('settings_app.urls')),
    path('api/media-pipeline/', include('media_pipeline.urls')),
    path('api/watchlist/', include('watchlist.urls')),
]
