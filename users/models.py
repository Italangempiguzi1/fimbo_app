import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        VIEWER = 'viewer', 'Viewer'
        CREATOR = 'creator', 'Creator'
        STAFF = 'staff', 'Staff'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=30, blank=True)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.VIEWER)
    avatar_url = models.URLField(blank=True)
    is_email_verified = models.BooleanField(default=False)
    is_phone_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.username or self.email
