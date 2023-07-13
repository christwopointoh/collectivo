"""Setup function for the profiles extension."""
from django.conf import settings
from django.contrib.auth import get_user_model

from collectivo.extensions.models import Extension
from collectivo.utils.dev import DEV_MEMBERS

from .apps import ProfilesConfig
from .models import ProfileSettings, ProfileSettingsField, UserProfile

User = get_user_model()


def setup(sender, **kwargs):
    """Initialize extension after database is ready."""

    Extension.objects.register(
        name=ProfilesConfig.name,
        description=ProfilesConfig.description,
        built_in=True,
    )

    # Initialize settings
    ProfileSettings.object()

    # Create default profile fields
    fields = [
        "person_type",
        "gender",
        "birthday",
        "legal_name",
        "legal_form",
        "legal_id",
        "address_street",
        "address_number",
        "address_stair",
        "address_door",
        "address_postcode",
        "address_city",
        "address_country",
        "phone",
    ]
    for field in fields:
        ProfileSettingsField.objects.get_or_create(
            name=field, label=field.capitalize().replace("_", " ")
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
