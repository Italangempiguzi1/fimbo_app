from django.db import models
from core.models import TimeStampedUUIDModel


class LegalPage(TimeStampedUUIDModel):
    class PageType(models.TextChoices):
        PRIVACY = 'privacy', 'Privacy Policy'
        TERMS = 'terms', 'Terms of Service'
        LICENSES = 'licenses', 'Licenses'
        HELP = 'help', 'Help Center'

    slug = models.SlugField(unique=True)
    title = models.CharField(max_length=160)
    page_type = models.CharField(max_length=30, choices=PageType.choices)
    body = models.TextField()
    language = models.CharField(max_length=10, default='en')
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ['page_type', 'title']

    def __str__(self):
        return self.title


class HelpArticle(TimeStampedUUIDModel):
    title = models.CharField(max_length=160)
    body = models.TextField()
    category = models.CharField(max_length=80, blank=True)
    language = models.CharField(max_length=10, default='en')
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ['category', 'title']
