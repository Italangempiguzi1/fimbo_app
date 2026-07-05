from django.contrib import admin
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'provider', 'status', 'amount', 'currency', 'created_at')
    list_filter = ('provider', 'status', 'currency')
    search_fields = ('user__username', 'user__email', 'provider_reference', 'phone')
