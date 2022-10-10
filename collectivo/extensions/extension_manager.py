"""Manager for installed extensions."""
from django.apps import apps


class ExtensionManager:
    """
    Manager for installed extensions.

    An extension is a django app that has an attribute 'collectivo_extension'
    that is set to True within its AppConfig class.
    """

    def __init__(self):
        """Load extensions."""
        self._extensions = []

        for app in apps.get_app_configs():
            if hasattr(app, 'collectivo_extension') \
                    and app.collectivo_extension == True:
                self._extensions.append(app)

    def get_configs(self):
        """Return a list of AppConfig objects for each extension."""
        return self._extensions.copy()


# This object is a global instance of ExtensionManager
# that can be imported and used by other modules.
extensions = ExtensionManager()
