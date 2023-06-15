"""Configuration file for the memberships_emails extension."""
from django.apps import AppConfig


class ExtensionConfig(AppConfig):
    """Configuration class for the extension."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "collectivo.memberships.emails"
    label = "memberships_emails"
    description = "Connect the memberships and emails extensions."
