"""Configuration file for the members extension."""
from django.apps import AppConfig
from django.db.models.signals import post_migrate
from collectivo.version import __version__


def post_migrate_callback(sender, **kwargs):
    """Initialize extension after database is ready."""
    from collectivo.extensions.utils import register_extension
    from collectivo.ux.utils import register_menuitem, register_microfrontend

    name = 'members'
    # TODO Language change
    # TODO Error handling
    # TODO Path handling
    # TODO Test put and patch
    # TODO Role filtering menu

    register_extension(
        name=name,
        version=__version__,
        description='An extension to manage member data and registration.'
    )

    register_microfrontend(
        name='members_user_ui',
        extension=name,
        path='http://localhost:8001/hardcoded/path/remoteEntry.js',
        type='modules'
    )

    register_microfrontend(
        name='members_admin_ui',
        extension=name,
        path='http://localhost:8001/hardcoded/path/remoteEntry.js',
        type='modules'
    )

    register_menuitem(
        name='members_user_menu_item',
        label='My membership',
        extension=name,
        menu='main_menu',
        microfrontend='members_user_ui'
    )

    register_menuitem(
        name='members_admin_menu_item',
        label='Member data',
        extension=name,
        menu='main_menu',
        microfrontend='members_admin_ui'
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
