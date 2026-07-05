from django.contrib import admin
from .models import BrandPlacement

@admin.register(BrandPlacement)
class BrandPlacementAdmin(admin.ModelAdmin):
    list_display = ('title', 'placement', 'sort_order', 'is_active', 'starts_at', 'ends_at')
    list_filter = ('placement', 'is_active')
    search_fields = ('title', 'subtitle')
