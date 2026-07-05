from django.contrib import admin
from .models import CreatorApplication

@admin.register(CreatorApplication)
class CreatorApplicationAdmin(admin.ModelAdmin):
    list_display = ('display_name', 'user', 'content_type', 'status', 'created_at')
    list_filter = ('status', 'content_type')
    search_fields = ('display_name', 'full_name', 'phone', 'email')
