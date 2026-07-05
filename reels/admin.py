from django.contrib import admin
from .models import Reel

@admin.register(Reel)
class ReelAdmin(admin.ModelAdmin):
    list_display = ('title', 'creator', 'status', 'total_views', 'total_likes', 'total_shares', 'created_at')
    list_filter = ('status', 'category')
    search_fields = ('title', 'caption', 'creator__display_name')
    readonly_fields = ('recommendation_score', 'total_views', 'total_watch_seconds', 'total_likes', 'total_comments', 'total_votes', 'total_awards', 'total_shares')
