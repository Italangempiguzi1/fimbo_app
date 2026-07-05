from django.contrib import admin
from .models import Category, Content, VideoAsset


class VideoAssetInline(admin.StackedInline):
    model = VideoAsset
    extra = 0


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_active')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = ('title', 'content_type', 'creator', 'status', 'is_featured', 'is_trending', 'total_views', 'created_at')
    list_filter = ('content_type', 'status', 'is_featured', 'is_trending', 'language', 'age_rating')
    search_fields = ('title', 'description', 'creator__display_name')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('recommendation_score', 'total_views', 'total_watch_seconds', 'total_likes', 'total_comments', 'total_votes', 'total_awards')
    inlines = [VideoAssetInline]


@admin.register(VideoAsset)
class VideoAssetAdmin(admin.ModelAdmin):
    list_display = ('content', 'quality_label', 'processing_status', 'updated_at')
    list_filter = ('processing_status', 'quality_label')
