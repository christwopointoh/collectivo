"""Utility functions for setting up extensions."""
import logging

from django.db.models.signals import post_migrate

logger = logging.getLogger(__name__)

# TODO: Check if there is a models.py file to trigger signal


def register_setup(function, appconfig, **kwargs):
    """Initialize extension after database is ready."""

    def perform_setup(sender, **signal_kwargs):
        try:
            function(**kwargs)
        except Exception as e:
            logger.error(
                f"Error while setting up extension {appconfig.name}: {e}",
                exc_info=True,
            )

    post_migrate.connect(perform_setup, sender=appconfig)
