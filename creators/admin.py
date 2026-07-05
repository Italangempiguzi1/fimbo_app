from django.contrib import admin
from .models import CreatorProfile


@admin.register(CreatorProfile)
class CreatorProfileAdmin(admin.ModelAdmin):
    list_display = ('display_name', 'user', 'verification_status', 'total_followers', 'is_active')
    list_filter = ('verification_status', 'is_active')
    search_fields = ('display_name', 'user__username', 'user__email')
