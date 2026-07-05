from django.urls import path
from .views import AwardAPIView, CommentListCreateAPIView, ToggleFollowAPIView, ToggleLikeAPIView, VoteAPIView

urlpatterns = [
    path('likes/toggle/', ToggleLikeAPIView.as_view(), name='like-toggle'),
    path('votes/', VoteAPIView.as_view(), name='vote'),
    path('follows/toggle/', ToggleFollowAPIView.as_view(), name='follow-toggle'),
    path('comments/', CommentListCreateAPIView.as_view(), name='comments'),
    path('awards/', AwardAPIView.as_view(), name='award'),
]
