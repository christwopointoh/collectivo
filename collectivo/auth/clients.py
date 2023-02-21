"""Testing clients of the authentication module."""
from rest_framework.test import APIClient, ForceAuthClientHandler
from collectivo.utils import get_auth_manager
from .userinfo import UserInfo


class AuthClientHandler(ForceAuthClientHandler):
    """Force authentication client handler for AuthClient."""

    def get_response(self, request):
        """Set forced user as user attribute."""
        request.userinfo = self._force_user if self._force_user else UserInfo()
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

    def __init__(self, force=False, enforce_csrf_checks=False, **defaults):
        """Initialize client with custom handler."""
        super().__init__(enforce_csrf_checks, **defaults)
        if force:
            self.handler = AuthClientHandler(enforce_csrf_checks)
            self.force_authenticate()

    def force_roles(self, roles: list):
        """Force authentication with passed role or roles."""
        user = UserInfo(roles=roles, is_authenticated=True)
        self.force_authenticate(user)

    def authorize(self, email: str, password: str = "Test123!"):
        """Authorize test user with the auth service."""
        auth_manager = get_auth_manager()
        token = auth_manager.openid.token(email, password)
        self.credentials(HTTP_AUTHORIZATION=token["access_token"])
