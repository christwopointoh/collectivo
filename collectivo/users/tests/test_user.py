"""Test the user model of the auth module."""
from django.test import TestCase
from ..clients import AuthClient
from collectivo.users.models import User
from collectivo.users.services import AuthToken
from collectivo.users.services import AuthService, AuthToken
from collectivo.users.exceptions import AuthDeleteError, AuthGetError
from .fixtures import TEST_USER, EMAIL, PASSWORD, PUBLIC_URL


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
        except AuthDeleteError:
            pass

    def test_get_token(self):
        """Test that a user token can be created."""
        self.user = User.objects.create(**TEST_USER)
        self.user.set_password(PASSWORD, temporary=False)
        self.user.set_email_verified(True)
        self.assertIsInstance(self.user.get_token(PASSWORD), AuthToken)

    def test_email_verification_needed(self):
        """Test that email verification is needed to get a token."""
        self.user = User.objects.create(**TEST_USER)
        self.user.set_password(PASSWORD, temporary=False)
        with self.assertRaises(AuthGetError):
            self.user.get_token(PASSWORD)

    def test_auto_create_user_in_auth_service(self):
        """Test that creating a user in collectivo also creates a user account
        of the authentication service."""
        user = User.objects.create(**TEST_USER)
        auth_service_user = self.auth_service.get_user(user.user_id)
        self.assertEqual(user.email, auth_service_user.email)

    def test_auto_update_user_in_auth_service(self):
        """Test that updating a user in collectivo also updates the user
        account of the authentication service."""
        user = User.objects.create(**TEST_USER)
        user.first_name = "New name"
        user.save()
        auth_service_user = self.auth_service.get_user(user.user_id)
        self.assertEqual(user.first_name, auth_service_user.first_name)

    def test_auto_create_user_in_collectivo(self):
        """Test that if a user from the authentication service is not a user in
        collectivo and makes an API call, a user in collectivo is created."""
        user_id = self.auth_service.create_user(
            **TEST_USER, email_verified=True
        )
        self.auth_service.set_user_password(user_id, PASSWORD, temporary=False)
        self.client.authorize(EMAIL, PASSWORD)
        user = User.objects.filter(email=EMAIL)
        self.assertFalse(user.exists())

        self.client.get(PUBLIC_URL)
        user = User.objects.get(email=EMAIL)
        for key, value in TEST_USER.items():
            self.assertEqual(getattr(user, key), value)
