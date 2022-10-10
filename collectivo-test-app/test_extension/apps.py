"""Configuration file for the test_extension extension."""

from django.apps import AppConfig


class TestExtensionConfig(AppConfig):
    """Configuration class for the test_extension extension."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'test_extension'

    # This registers the app as a collectivo extension
    collectivo_extension = True
