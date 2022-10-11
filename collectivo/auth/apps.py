"""Configuration file for the auth extension."""
from django.apps import AppConfig


class AuthConfig(AppConfig):
    """Configuration class of the auth extension."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'collectivo.auth'
