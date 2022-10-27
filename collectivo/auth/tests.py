"""Test the keycloak authentication module."""
from django.test import TestCase, RequestFactory
from django.conf import settings
from keycloak import KeycloakOpenID
from .middleware import KeycloakMiddleware
from rest_framework.test import APIClient
from django.urls import reverse


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
        self.token = self.keycloak.token('test_member_1', 'test')
        self.access_token = 'Token ' + self.token['access_token']
        self.middleware = KeycloakMiddleware(None)
        self.factory = RequestFactory()
        self.private_endpoint = 'collectivo:collectivo.auth:private'
        self.public_endpoint = 'collectivo:collectivo.auth:test_public'

    def test_middleware_correct_token(self):
        """Test passing a correct token to the middleware."""
        request = self.factory.get('', HTTP_AUTHORIZATION=self.access_token)
        self.middleware.process_view(request, None, None, None)
        self.assertTrue(request.is_authenticated)

    def test_middleware_bad_token(self):
        """Test passing a bad token to the middleware."""
        request = self.factory.get('', HTTP_AUTHORIZATION='Token badtoken')
        self.middleware.process_view(request, None, None, None)
        self.assertFalse(request.is_authenticated)

    def test_middleware_bad_token_2(self):
        """Test passing a empty auth string to the middleware."""
        request = self.factory.get('', HTTP_AUTHORIZATION='')
        self.middleware.process_view(request, None, None, None)
        self.assertFalse(request.is_authenticated)

    def test_middleware_bad_token_3(self):
        """Test passing a faulty auth string to the middleware."""
        request = self.factory.get('', HTTP_AUTHORIZATION='bad bad bad')
        self.middleware.process_view(request, None, None, None)
        self.assertFalse(request.is_authenticated)

    def test_middleware_bad_token_4(self):
        """Test passing a faulty auth string to the middleware."""
        request = self.factory.get('', HTTP_AUTHORIZATION='Token')
        self.middleware.process_view(request, None, None, None)
        self.assertFalse(request.is_authenticated)

    def test_middleware_no_token(self):
        """Test passing an authenticated request to the middleware."""
        request = self.factory.get('', HTTP_AUTHORIZATION='Token badtoken')
        self.middleware.process_view(request, None, None, None)
        self.assertFalse(request.is_authenticated)

    def test_private_api_with_correct_token(self):
        """Test that private api call with correct token succeeds."""
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=self.access_token)
        res = client.get(reverse(self.private_endpoint))
        self.assertEqual(res.status_code, 200)

    def test_private_api_with_bad_token(self):
        """Test that private api call with bad token fails."""
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + 'bad_token')
        res = client.get(reverse(self.private_endpoint))
        self.assertEqual(res.status_code, 401)

    def test_private_api_with_no_token(self):
        """Test that private api call with no token fails."""
        client = APIClient()
        res = client.get(reverse(self.private_endpoint))
        self.assertEqual(res.status_code, 403)

    def test_public_api_with_correct_token(self):
        """Test that public api call with correct token succeeds."""
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=self.access_token)
        res = client.get(reverse(self.public_endpoint))
        self.assertEqual(res.status_code, 200)

    def test_public_api_with_bad_token(self):
        """Test that public api call with bad token fails."""
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + 'bad_token')
        res = client.get(reverse(self.public_endpoint))
        self.assertEqual(res.status_code, 401)

    def test_public_api_with_no_token(self):
        """Test that public api call with no token succeeds."""
        client = APIClient()
        res = client.get(reverse(self.public_endpoint))
        self.assertEqual(res.status_code, 200)
