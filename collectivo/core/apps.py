"""Configuration file of the core extension."""
from django.apps import AppConfig

from collectivo.utils.setup import register_setup


class CoreConfig(AppConfig):
    """Configuration class of the menus module."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "collectivo.core"
    description = "Core of collectivo."

    def ready(self):
        """
        Initialize app when it is ready.

        Database calls are performed after migrations, using the post_migrate
        signal. This signal only works if the app has a models.py module.
        """
        from . import signals  # noqa: F401
        from .setup import setup

        register_setup(setup, self)
