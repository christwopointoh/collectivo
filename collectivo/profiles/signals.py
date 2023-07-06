"""Signals of the profiles extension."""
from django.contrib.auth import get_user_model
from django.db.models import signals

from .models import UserProfile


def create_user_profile(sender, instance, created, **kwargs):
    """Create user profile when a user is created."""
    UserProfile.objects.get_or_create(user=instance)


signals.post_save.connect(
    create_user_profile,
    sender=get_user_model(),
    dispatch_uid="create_user_profile",
    weak=False,
)
