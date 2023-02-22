"""Testing clients of the authentication module."""
from rest_framework.test import APIClient, ForceAuthClientHandler
from collectivo.users.services import AuthService
from collectivo.users.models import User


class CustomForceAuthClientHandler(ForceAuthClientHandler):
    """Handler to force authentication with the user object."""

    def get_response(self, request):
        """Set forced user as user attribute."""
        request.auth_user = self._force_user if self._force_user else User()
        return super().get_response(request)


class AuthClient(APIClient):
    """
    APIClient that can authenticate with the auth module's userinfo.

    Usage example:
    ```
        client = CollectivoAPIClient()
        user = {
            'sub': 'ac4339c5-56f6-4df5-a6c8-bcdd3683a56a',
            'roles': ['test_role'],
            'email': 'test_member_1@example.com'
        }
        client.force_authenticate(user)
    ```
    """

    def __init__(self, force=True, enforce_csrf_checks=False, **defaults):
        """Initialize client with custom handler."""
        super().__init__(enforce_csrf_checks, **defaults)

    def force_authenticate(self, user=None):
        """Force authentication with passed user or token."""
        self.handler = CustomForceAuthClientHandler()
        super().force_authenticate(user)
        # TODO: Roles

    def authorize(self, email: str, password: str = "Test123!"):
        """Authorize test user with the auth service."""
        auth_service = AuthService()
        token = auth_service.openid.token(email, password)
        self.credentials(HTTP_AUTHORIZATION=token["access_token"])
