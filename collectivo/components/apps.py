"""Configuration file for the components module.."""
from django.apps import AppConfig
from django.db.models.signals import post_migrate


class ComponentsConfig(AppConfig):
    """Configuration class of the components module."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "collectivo.components"
    description = "Manage frontend components of collectivo."

    def ready(self):
        """
        Initialize app when it is ready.

        Database calls are performed after migrations, using the post_migrate
        signal. This signal only works if the app has a models.py module.
        """
        from .setup import setup

        post_migrate.connect(setup, sender=self)
