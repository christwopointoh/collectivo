"""Utility functions of the authentication module."""
from rest_framework.test import APIClient, ForceAuthClientHandler


class KeycloakForceAuthClientHandler(ForceAuthClientHandler):
    """Force authentication client handler for KeyCloakAPIClient."""

    def get_response(self, request):
        """Set forced user as userinfo attribute."""
        request.userinfo = self._force_user
        return super().get_response(request)


class KeycloakAPIClient(APIClient):
    """
    APIClient that can force authentication for KeycloakMiddleware.

    Usage example:
    ```
        client = KeycloakAPIClient()
        user = {
            'sub': 'ac4339c5-56f6-4df5-a6c8-bcdd3683a56a',
            'roles': ['test_role'],
            'email': 'test_member_1@example.com'
        }
        client.force_authenticate(user)
    ```
    """

    def __init__(self, enforce_csrf_checks=False, **defaults):
        """Initialize parent client with custom handler."""
        super().__init__(**defaults)
        self.handler = KeycloakForceAuthClientHandler(enforce_csrf_checks)
