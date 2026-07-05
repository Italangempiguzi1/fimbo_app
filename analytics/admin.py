from django.contrib import admin
from .models import WatchSession


@admin.register(WatchSession)
class WatchSessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'creator', 'target_type', 'seconds_watched', 'is_valid_view', 'started_at')
    list_filter = ('target_type', 'is_valid_view', 'completed')
    search_fields = ('user__username', 'user__email', 'creator__display_name')
