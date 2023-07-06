"""Setup function for the profiles extension."""
from django.conf import settings
from django.contrib.auth import get_user_model

from collectivo.extensions.models import Extension
from collectivo.utils.dev import DEV_MEMBERS

from .apps import ProfilesConfig
from .models import UserProfile

User = get_user_model()


def setup(sender, **kwargs):
    """Initialize extension after database is ready."""

    Extension.objects.register(
        name=ProfilesConfig.name,
        description=ProfilesConfig.description,
        built_in=True,
    )

    # Create missing profiles
    users = User.objects.filter(profile__isnull=True)
    for user in users:
        UserProfile.objects.get_or_create(user=user)

    if settings.COLLECTIVO["example_data"] is True:
        for first_name in DEV_MEMBERS:
            email = f"test_{first_name}@example.com"
            user = get_user_model().objects.get(email=email)
            UserProfile.objects.get_or_create(user=user)
