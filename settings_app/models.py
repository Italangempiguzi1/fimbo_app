from django.conf import settings
from django.db import models
from core.models import TimeStampedUUIDModel


class UserPreference(TimeStampedUUIDModel):
    class Theme(models.TextChoices):
        SYSTEM = 'system', 'System'
        DARK = 'dark', 'Dark'
        LIGHT = 'light', 'Light'

    class Language(models.TextChoices):
        EN = 'en', 'English'
        SW = 'sw', 'Kiswahili'

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='preferences')
    theme = models.CharField(max_length=20, choices=Theme.choices, default=Theme.DARK)
    language = models.CharField(max_length=10, choices=Language.choices, default=Language.EN)
    autoplay_reels = models.BooleanField(default=True)
    download_quality = models.CharField(max_length=20, default='720p')
    push_notifications = models.BooleanField(default=True)
    email_notifications = models.BooleanField(default=True)

    def __str__(self):
        return f'Preferences for {self.user}'
