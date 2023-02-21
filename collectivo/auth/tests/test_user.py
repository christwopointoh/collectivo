"""Test the user model of the auth module."""
from django.test import TestCase
from django.urls import reverse
from ..clients import AuthClient
from collectivo.auth.models import User
from collectivo.auth.services import AuthService
from collectivo.auth.exceptions import AuthDeleteError

EMAIL = "test_user@example.com"
PASSWORD = "Test123!"
TEST_USER = {
    "first_name": "Test",
    "last_name": "User",
    "email": EMAIL,
}
TEST_URL = reverse("collectivo:collectivo.auth:test_view_public")


class AuthUserTests(TestCase):
    """Test the user model of the authentication module."""

    def setUp(self):
        """Set up test client."""

        self.client = AuthClient()
        self.auth_service = AuthService()
        self.tearDown()

    def tearDown(self):
        """Delete test user."""
        try:
            self.auth_service.delete_user(self.auth_service.get_user_id(EMAIL))
        except AuthDeleteError as e:
            pass

    def test_create_user_manually(self):
        """Test that creating a user in collectivo also creates a user account
        at the authentication service."""
        user = User.objects.create(**TEST_USER)
        auth_service_user = self.auth_service.get_user(user.user_id)
        self.assertEqual(user.email, auth_service_user.email)

    def test_create_user_automatically(self):
        """Test that if a user from the authentication service is not a user in
        collectivo and makes an API call, a user in collectivo is created."""
        user_id = self.auth_service.create_user(
            **TEST_USER, email_verified=True
        )
        self.auth_service.set_user_password(user_id, PASSWORD, temporary=False)
        self.client.authorize(EMAIL, PASSWORD)
        user = User.objects.filter(email=EMAIL)
        self.assertFalse(user.exists())

        self.client.get(TEST_URL)
        user = User.objects.get(email=EMAIL)
        for key, value in TEST_USER.items():
            self.assertEqual(getattr(user, key), value)
