"""Tests of the members API."""
from uuid import UUID
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from collectivo.auth.utils import KeycloakAPIClient
from ..models import Member


MEMBERS_URL = reverse('collectivo:collectivo.members:member-list')
ME_URL = reverse('collectivo:collectivo.members:me')


class PublicRecipeApiTests(TestCase):
    """Test unauthenticated members API access."""

    def setUp(self):
        """Prepare client."""
        self.client = APIClient()

    def test_auth_required_for_members(self):
        """Test that authentication is required."""
        res = self.client.get(MEMBERS_URL)
        self.assertEqual(res.status_code, 403)

    def test_auth_required_for_me(self):
        """Test that authentication is required."""
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, 403)


class PrivateMemberApiTests(TestCase):
    """Test the privatly available members API for members."""

    def setUp(self):
        """Prepare client."""
        self.client = KeycloakAPIClient()
        self.user = {
            'sub': 'ac4339c5-56f6-4df5-a6c8-bcdd3683a56a',
            'roles': ['members_user'],
            'email': 'test_member_1@example.com'
        }
        self.payload = {
            'user_attr': '1',
            'create_attr': '2',
            'admin_attr': '3'
        }
        self.expected_userinfo = {
            **self.payload,
            'admin_attr': 'default value',
            'user_id': UUID(self.user['sub'])
        }
        self.client.force_authenticate(self.user)

    def test_member_cannot_access_admin_area(self):
        """Test that a normal member cannot access admin API."""
        res = self.client.get(MEMBERS_URL)
        self.assertEqual(res.status_code, 403)

    def test_create_member_as_user(self):
        """Test that an authenticated user can create itself as a member."""
        res = self.client.post(ME_URL, self.payload)
        self.assertEqual(res.status_code, 201)
        member = Member.objects.get(id=res.data['id'])

        for key in self.expected_userinfo.keys():
            self.assertEqual(self.expected_userinfo[key], getattr(member, key))

    def test_cannot_create_same_member_twice(self):
        """Test that a member cannot create itself as a member again."""
        res = self.client.post(ME_URL, self.payload)
        self.assertEqual(res.status_code, 201)
        res2 = self.client.post(ME_URL, self.payload)
        self.assertEqual(res2.status_code, 403)

    def test_get_own_member(self):
        """Test that a member can view it's own data."""
        self.client.post(ME_URL, self.payload)
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, 200)
        for key in self.expected_userinfo.keys():
            self.assertEqual(str(self.expected_userinfo[key]), res.data[key])

    def test_get_member_fails_if_not_exists(self):
        """Test that a user cannot access API if they are not a member."""
        res2 = self.client.get(ME_URL)
        self.assertEqual(res2.status_code, 404)

    def test_update_member(self):
        """Test that a member can edit non-admin fields of it's own data."""
        res1 = self.client.post(ME_URL, self.payload)
        res2 = self.client.put(ME_URL, {'user_attr': 'new_value'})
        self.assertEqual(res2.status_code, 200)
        member = Member.objects.get(id=res1.data['id'])
        self.assertEqual(getattr(member, 'user_attr'), 'new_value')

    def test_update_member_create_fields_fails(self):
        """Test that a member cannot edit admin fields of it's own data."""
        res1 = self.client.post(ME_URL, self.payload)
        res2 = self.client.put(ME_URL, {'create_attr': 'new_value'})
        self.assertEqual(res2.status_code, 400)
        member = Member.objects.get(id=res1.data['id'])
        self.assertNotEqual(getattr(member, 'create_attr'), 'new_value')

    def test_update_member_admin_fields_fails(self):
        """Test that a member cannot edit admin fields of it's own data."""
        res1 = self.client.post(ME_URL, self.payload)
        res2 = self.client.put(ME_URL, {'admin_attr': 'new_value'})
        self.assertEqual(res2.status_code, 400)
        member = Member.objects.get(id=res1.data['id'])
        self.assertNotEqual(getattr(member, 'admin_attr'), 'new_value')


class AdminMemberApiTests(TestCase):
    """Test the privatly available members API for admins."""

    def setUp(self):
        """Prepare client, extension, & micro-frontend."""
        self.client = KeycloakAPIClient()
        userinfo = {
            'sub': 'ac4339c5-56f6-4df5-a6c8-bcdd3683a56a',
            'roles': ['members_admin'],
            'email': 'test_member_1@example.com'
        }
        self.client.force_authenticate(userinfo)
        self.payload = {
            'user_attr': '1',
            'create_attr': '2',
            'admin_attr': '3'
        }

    def create_members(self, n_users):
        """Create a set of members for testing."""
        for i, user in enumerate(range(n_users)):
            payload = {**self.payload, 'user_attr': str(i)}
            self.client.post(MEMBERS_URL, payload)

    def test_create_members(self):
        """Test that admins can create members with access to all fields."""
        n_users = 5
        self.create_members(n_users)
        self.assertEqual(len(Member.objects.all()), n_users)

    def test_update_member_admin_fields(self):
        """Test that only admins can write to admin fields."""
        res1 = self.client.post(MEMBERS_URL, self.payload)
        res2 = self.client.patch(
            reverse(
                'collectivo:collectivo.members:member-detail',
                args=[res1.data['id']]),
            {'admin_attr': 'new_value'}
        )
        self.assertEqual(res2.status_code, 200)
        member = Member.objects.get(id=res1.data['id'])
        self.assertEqual(getattr(member, 'admin_attr'), 'new_value')

    def test_member_sorting(self):
        """Test that all member fields can be sorted."""
        n_users = 3
        self.create_members(n_users)

        res = self.client.get(MEMBERS_URL+'?orderingx=user_attr')
        self.assertEqual(
            [entry['user_attr'] for entry in res.data],
            ['0', '1', '2']
        )

        res = self.client.get(MEMBERS_URL+'?ordering=-user_attr')
        self.assertEqual(
            [entry['user_attr'] for entry in res.data],
            ['2', '1', '0']
        )

    def test_member_filtering(self):
        """Test that all member fields can be filtered."""
        n_users = 3
        self.create_members(n_users)

        res = self.client.get(MEMBERS_URL+'?user_attr=1')
        self.assertEqual(
            [entry['user_attr'] for entry in res.data],
            ['1']
        )

        res = self.client.get(MEMBERS_URL+'?user_attr__gte=1')
        self.assertEqual(
            [entry['user_attr'] for entry in res.data],
            ['1', '2']
        )

        res = self.client.get(MEMBERS_URL+'?user_attr__contains=1')
        self.assertEqual(
            [entry['user_attr'] for entry in res.data],
            ['1']
        )

    def test_member_pagination(self):
        """Test that pagination works for members."""
        n_users = 10
        self.create_members(n_users)

        limit = 3
        offset = 5
        res = self.client.get(
            MEMBERS_URL+f'?limit={limit}&offset={offset}')

        self.assertEqual(
            [m.id for m in Member.objects.all()][offset:offset+limit],
            [m['id'] for m in res.data['results']]
        )
