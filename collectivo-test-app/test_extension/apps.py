"""Configuration file for the test_extension extension."""

from django.apps import AppConfig


class TestExtensionConfig(AppConfig):
    """Configuration class for the test_extension extension."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'test_extension'

    def ready(self):
        """Import modules that should be loaded at start."""
        from . import menus, urls  # noqa
