"""Configuration file for the collectivo extensions module."""
from django.apps import AppConfig


class ExtensionsConfig(AppConfig):
    """Configuration class of the collectivo extensions module."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'collectivo.extensions'
