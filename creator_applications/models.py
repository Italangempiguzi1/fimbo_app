from django.conf import settings
from django.db import models
from core.models import TimeStampedUUIDModel


class CreatorApplication(TimeStampedUUIDModel):
    class Status(models.TextChoices):
        DRAFT = 'draft', 'Draft'
        SUBMITTED = 'submitted', 'Submitted'
        APPROVED = 'approved', 'Approved'
        REJECTED = 'rejected', 'Rejected'

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='creator_application')
    full_name = models.CharField(max_length=180)
    display_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=30)
    email = models.EmailField()
    business_name = models.CharField(max_length=180, blank=True)
    content_type = models.CharField(max_length=160)
    portfolio_url = models.URLField(blank=True)
    id_document = models.FileField(upload_to='creator_applications/id_documents/', null=True, blank=True)
    message = models.TextField(blank=True)
    agreed_to_terms = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.SUBMITTED)
    review_note = models.TextField(blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.display_name} - {self.status}'
