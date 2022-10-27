"""Configuration file for the authentication module."""
from django.apps import AppConfig


class AuthConfig(AppConfig):
    """Configuration class of the authentication module."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'collectivo.auth'
    label = 'collectivo_auth'
