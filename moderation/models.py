import uuid
from django.conf import settings
from django.db import models
from core.models import TimeStampedUUIDModel
from engagement.models import TargetType


class Report(TimeStampedUUIDModel):
    class Reason(models.TextChoices):
        COPYRIGHT = 'copyright', 'Copyright'
        HARMFUL = 'harmful', 'Harmful Content'
        HATE = 'hate', 'Hate or Harassment'
        SEXUAL = 'sexual', 'Sexual Content'
        SPAM = 'spam', 'Spam or Scam'
        OTHER = 'other', 'Other'

    class Status(models.TextChoices):
        OPEN = 'open', 'Open'
        REVIEWING = 'reviewing', 'Reviewing'
        RESOLVED = 'resolved', 'Resolved'
        REJECTED = 'rejected', 'Rejected'

    reporter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reports')
    target_type = models.CharField(max_length=20, choices=TargetType.choices)
    target_id = models.UUIDField(default=uuid.uuid4)
    reason = models.CharField(max_length=30, choices=Reason.choices)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.OPEN)

    class Meta:
        ordering = ['-created_at']


class ModerationAction(TimeStampedUUIDModel):
    class ActionType(models.TextChoices):
        APPROVE = 'approve', 'Approve'
        REJECT = 'reject', 'Reject'
        HIDE = 'hide', 'Hide'
        RESTORE = 'restore', 'Restore'
        SUSPEND_CREATOR = 'suspend_creator', 'Suspend Creator'
        TAKEDOWN = 'takedown', 'Takedown'

    moderator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='moderation_actions')
    report = models.ForeignKey(Report, on_delete=models.SET_NULL, related_name='actions', null=True, blank=True)
    target_type = models.CharField(max_length=20, choices=TargetType.choices)
    target_id = models.UUIDField(default=uuid.uuid4)
    action_type = models.CharField(max_length=30, choices=ActionType.choices)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-created_at']
