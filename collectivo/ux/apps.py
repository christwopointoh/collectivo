"""Configuration file of the user experience module."""
from django.apps import AppConfig
from django.db.models.signals import post_migrate


def post_migrate_callback(sender, **kwargs):
    """Initialize extension after database is ready."""
    from .utils import register_menu

    register_menu('main_menu')


class CollectivoUxConfig(AppConfig):
    """Configuration class of the user experience module."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'collectivo.ux'

    def ready(self):
        """
        Initialize app when it is ready.

        Database calls are performed after migrations, using the post_migrate
        signal. This signal only works if the app has a models.py module.
        """
        post_migrate.connect(post_migrate_callback, sender=self)
