"""Tests for the authentication client."""
from django.test import TestCase
from django.urls import reverse
from ..clients import AuthClient
from django.test import TestCase
from django.urls import reverse
from ..clients import AuthClient
from collectivo.auth.models import User, AnonymousUser
from .fixtures import TEST_USER, EMAIL, PASSWORD, PRIVATE_URL


class AuthClientTests(TestCase):
    """Tests for the authentication client."""

    def setUp(self):
        """Prepare client and keycloak token."""
        self.client: AuthClient = AuthClient()

    def test_force_authentication_succeeds(self):
        """Test force authentication with normal user succeeds."""
        self.client.force_authenticate(User())
        res = self.client.get(PRIVATE_URL)
        self.assertEqual(res.status_code, 200)

    def test_force_authentication_fails(self):
        """Test force authentication with anonymous user fails."""
        self.client.force_authenticate(AnonymousUser())
        res = self.client.get(PRIVATE_URL)
        self.assertEqual(res.status_code, 403)

    def test_authorize_fails(self):
        """Test that autorization with email and password fails."""
        res = self.client.get(PRIVATE_URL)
        self.assertEqual(res.status_code, 403)

    def test_authorize_succeeds(self):
        """Test that autorization with email and password succeeds."""
        self.user = User.objects.create(**TEST_USER)
        self.user.set_password(PASSWORD, temporary=False)
        self.user.set_email_verified(True)
        self.client.authorize(EMAIL, PASSWORD)
        res = self.client.get(PRIVATE_URL)
        self.assertEqual(res.status_code, 200)
