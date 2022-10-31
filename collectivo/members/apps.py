"""Configuration file for the members extension."""
from django.apps import AppConfig
from django.db.models.signals import post_migrate


def post_migrate_callback(sender, **kwargs):
    """Initialize extension after database is ready."""
    from collectivo.extensions.utils import register_extension
    from collectivo.ux.utils import register_microfrontend, register_menuitem

    register_extension(
        name=sender.name,
        version='0.0.1',
        description='This extension.'
    )

    register_menuitem(
        name='menuitem_'+sender.name+'_modules',
        label='Membership',
        extension=sender.name,
        menu='main_menu',
        microfrontend=sender.name+'_modules',
        requires_role='is_member'
    )

    register_menuitem(
        name='menuitem_'+sender.name+'_modules',
        label='Members (admin)',
        extension=sender.name,
        menu='main_menu',
        microfrontend=sender.name+'_modules',
        requires_role='is_members_admin'
    )

class MembersConfig(AppConfig):
    """Configuration class for the members extension."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'collectivo.members'

    def ready(self):
        """
        Initialize app when it is ready.

        Database calls are performed after migrations, using the post_migrate
        signal. This signal only works if the app has a models.py module.
        """
        post_migrate.connect(post_migrate_callback, sender=self)
