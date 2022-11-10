"""Tests of the members API."""
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from collectivo.auth.clients import CollectivoAPIClient
from collectivo.auth.userinfo import UserInfo


TILES_URL = reverse('collectivo:collectivo.dashboard:tiles')


class PublicDashboardApiTests(TestCase):
    """Test the public dashboard API."""

    def setUp(self):
        """Prepare client."""
        self.client = APIClient()

    def test_auth_required_for_members(self):
        """Test that authentication is required for /tiles."""
        res = self.client.get(TILES_URL)
        self.assertEqual(res.status_code, 403)


class PrivateDashboardApiTests(TestCase):
    """Test the private dashboard API."""

    def setUp(self):
        """Prepare client."""
        self.client = CollectivoAPIClient()
        self.user = UserInfo(
            user_id='ac4339c5-56f6-4df5-a6c8-bcdd3683a56a',
            email='some_member@example.com',
            is_authenticated=True,
        )
        self.client.force_authenticate(self.user)

    # def test_create_member_as_user(self):
    #     """Test that an authenticated user can create itself as a member."""
    #     res = self.client.post(ME_URL, self.payload)
    #     self.assertEqual(res.status_code, 201)
    #     member = Member.objects.get(id=res.data['id'])

    #     for key in self.expected_user.keys():
    #         self.assertEqual(self.expected_user[key], getattr(member, key))
