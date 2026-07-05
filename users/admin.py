from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'phone', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'phone')
    fieldsets = UserAdmin.fieldsets + (
        ('Umbrella fields', {'fields': ('phone', 'role', 'avatar_url', 'is_email_verified', 'is_phone_verified')}),
    )
