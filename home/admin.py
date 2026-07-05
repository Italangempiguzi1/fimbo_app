from django.contrib import admin
from .models import HeroBanner, HomeSection

@admin.register(HeroBanner)
class HeroBannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'target_type', 'sort_order', 'is_active')
    list_filter = ('target_type', 'is_active')
    search_fields = ('title', 'subtitle')

@admin.register(HomeSection)
class HomeSectionAdmin(admin.ModelAdmin):
    list_display = ('key', 'title', 'section_kind', 'content_type', 'sort_order', 'is_active')
    list_filter = ('section_kind', 'is_active')
