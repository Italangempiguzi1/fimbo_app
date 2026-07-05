from django.contrib import admin
from .models import Plan, Subscription


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'price_tzs', 'max_devices', 'max_quality', 'is_active')
    list_filter = ('is_active', 'downloads_enabled', 'early_access_enabled')
    search_fields = ('name', 'code')


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'plan', 'status', 'started_at', 'expires_at', 'auto_renew')
    list_filter = ('status', 'plan', 'auto_renew')
    search_fields = ('user__username', 'user__email', 'provider_reference')
