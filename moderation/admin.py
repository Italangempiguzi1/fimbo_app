from django.contrib import admin
from .models import ModerationAction, Report

admin.site.register(Report)
admin.site.register(ModerationAction)
