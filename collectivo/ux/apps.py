"""Configuration file for the collectivo ux extension."""
from django.apps import AppConfig


class CollectivoUxConfig(AppConfig):
    """Configuration class of the collectivo ux extension."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'collectivo.ux'

    def ready(self):
        """Import modules that should be loaded at start."""
        from . import urls  # noqa
