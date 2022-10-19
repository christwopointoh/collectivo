"""Configuration file of the user experience module."""
from django.apps import AppConfig


class CollectivoUxConfig(AppConfig):
    """Configuration class of the user experience module."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'collectivo.ux'
