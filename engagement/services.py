from django.shortcuts import get_object_or_404
from content.models import Content
from reels.models import Reel
from .models import TargetType


def get_target_or_404(target_type, target_id):
    if target_type == TargetType.CONTENT:
        return get_object_or_404(Content, id=target_id)
    if target_type == TargetType.REEL:
        return get_object_or_404(Reel, id=target_id)
    raise ValueError('Unsupported target type')


def get_target_creator(target_type, target_id):
    return get_target_or_404(target_type, target_id).creator


def increment_counter(target, field, amount=1):
    current = getattr(target, field, 0) or 0
    setattr(target, field, current + amount)
    target.save(update_fields=[field, 'updated_at'])
