"""Configuration file for the test_extension app."""
from django.apps import AppConfig
from django.db.models.signals import post_migrate


def post_migrate_callback(sender, **kwargs):
    """Initialize extension after database is ready."""
    from collectivo.extensions.utils import register_extension
    from .populate import populate_keycloak_with_test_data
    from collectivo.ux.utils import register_microfrontend, register_menuitem

    register_extension(
        name=sender.name,
        version='0.0.1',
        description='A test extension.'
    )

    register_microfrontend(
        name=sender.name+'_modules',
        extension=sender.name,
        path='http://collectivo.local:8000/static/test_extension/remoteEntry.js',
        type='modules'
    )

    register_microfrontend(
        name=sender.name+'_iframe',
        extension=sender.name,
        path='http://collectivo.local:8000/test_extension/',
        type='html'
    )

    register_menuitem(
        name='menuitem_'+sender.name+'_modules',
        label='Open test webcomponent',
        extension=sender.name,
        menu='main_menu',
        microfrontend=sender.name+'_modules'
    )

    register_menuitem(
        name='menuitem_'+sender.name+'_iframe',
        label='Open test iframe',
        extension=sender.name,
        menu='main_menu',
        microfrontend=sender.name+'_iframe'
    )

    populate_keycloak_with_test_data()


class TestExtensionConfig(AppConfig):
    """Configuration class for the test_extension app."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'test_extension'

    def ready(self):
        """
        Initialize app when it is ready.

        Database calls are performed after migrations, using the post_migrate
        signal. This signal only works if the app has a models.py module.
        """
        post_migrate.connect(post_migrate_callback, sender=self)
