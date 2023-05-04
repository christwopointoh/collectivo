"""Stores of collectivo."""


class MainStore:
    """A manager that can store information in memory."""

    def __init__(self):
        """Initialize the manager."""
        self.user_profiles_admin_serializers = []  # Used by core.serializers


# Store to be used for import by other extensions
main_store = MainStore()
