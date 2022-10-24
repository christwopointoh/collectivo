"""Test the keycloak authentication module."""
from django.test import TestCase, RequestFactory
from rest_framework.test import APIClient
from django.conf import settings
from keycloak import KeycloakOpenID
from .middleware import KeycloakMiddleware


class AuthenticationTests(TestCase):
    """Test the authentication of users through keycloak."""

    def setUp(self):
        """Prepare client and keycloak token."""
        config = settings.KEYCLOAK_CONFIG
        self.keycloak = KeycloakOpenID(
            server_url=config["SERVER_URL"],
            client_id=config["REALM_NAME"],
            realm_name=config["CLIENT_ID"],
            client_secret_key=config["CLIENT_SECRET_KEY"],
        )
        self.token = self.keycloak.token('testuser', 'test')
        self.access_token = 'Token ' + self.token['access_token']
        self.middleware = KeycloakMiddleware(None)
        self.factory = RequestFactory()
        # self.client = APIClient()
        # self.client.credentials(
        #     HTTP_AUTHORIZATION='Token ' + self.token['access_token'])

    def test_authenticated_request(self):
        """Test making an authenticated request."""
        request = self.factory.get('', HTTP_AUTHORIZATION=self.access_token)
        self.middleware.process_view(request, None, None, None)
        self.assertTrue(request.is_authenticated)

    def test_unauthenticated_request(self):
        """Test making an unauthenticated request."""
        request = self.factory.get('', HTTP_AUTHORIZATION='Token badtoken')
        self.middleware.process_view(request, None, None, None)
        self.assertFalse(request.is_authenticated)
