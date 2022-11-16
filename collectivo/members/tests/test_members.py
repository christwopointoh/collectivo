"""Tests of the members API."""
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from collectivo.auth.clients import CollectivoAPIClient
from collectivo.auth.userinfo import UserInfo
from collectivo.utils import get_auth_manager
from ..models import Member


MEMBERS_URL = reverse('collectivo:collectivo.members:member-list')
ME_URL = reverse('collectivo:collectivo.members:me')

TEST_MEMBER = {
    'first_name': 'firstname',
    'last_name': 'lastname',
    'email': 'some_member@example.com',
    'email_verified': True,
}

TEST_USER = {
    'email': 'some_member@example.com',
    'username': 'some_member@example.com',
    'firstName': 'firstname',
    'lastName': 'lastname',
    "enabled": True,
    "emailVerified": True,
}


class PublicMemberApiTests(TestCase):
    """Test the public members API."""

    def setUp(self):
        """Prepare client."""
        self.client = APIClient()

    def test_auth_required_for_members(self):
        """Test that authentication is required for /members."""
        res = self.client.get(MEMBERS_URL)
        self.assertEqual(res.status_code, 403)

    def test_auth_required_for_me(self):
        """Test that authentication is required for /me."""
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, 403)


class MembersTestCase(TestCase):
    """Template for test cases that need an authorized user."""

    def setUp(self):
        """Create client with authorized test user."""
        self.auth_manager = get_auth_manager()
        user_id = self.auth_manager.create_user(TEST_USER, exist_ok=True)
        self.auth_manager.set_user_password(  # noqa
                user_id, password='test', temporary=False)  # noqa
        self.client = APIClient()
        self.authorize()

    def tearDown(self):
        """Delete test user."""
        auth_manager = get_auth_manager()
        user_id = auth_manager.get_user_id('some_member@example.com')
        auth_manager.delete_user(user_id)

    def authorize(self):
        """Authorize test user."""
        token = self.auth_manager.openid.token(
            'some_member@example.com', 'test')
        self.client.credentials(HTTP_AUTHORIZATION=token['access_token'])


class PrivateMemberApiTestsForNonMembers(MembersTestCase):
    """Test the private members API for users that are not members."""

    def test_cannot_access_profile(self):
        """Test that a user cannot access API if they are not a member."""
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(res.data['detail'],
                         'User is not registered as a member.')

    def test_create_member(self):
        """Test that an authenticated user can create itself as a member."""
        res = self.client.post(ME_URL, TEST_MEMBER)
        self.assertEqual(res.status_code, 201)
        member = Member.objects.get(id=res.data['id'])
        expected_user = {**TEST_MEMBER}
        del expected_user['email_verified']  # not shown to user
        for key in expected_user.keys():
            self.assertEqual(expected_user[key], getattr(member, key))


class PrivateMemberApiTestsForMembers(MembersTestCase):
    """Test the private members API for users that are members."""

    def setUp(self):
        """Register authorized user as member."""
        super().setUp()
        res = self.client.post(ME_URL, TEST_MEMBER)
        self.authorize()  # Needed to refresh token with new role
        self.members_id = res.data['id']

    def test_member_cannot_access_admin_area(self):
        """Test that a normal member cannot access admin API."""
        res = self.client.get(MEMBERS_URL)
        self.assertEqual(res.status_code, 403)

    def test_cannot_create_same_member_twice(self):
        """Test that a member cannot create itself as a member again."""
        res2 = self.client.post(ME_URL, TEST_MEMBER)
        self.assertEqual(res2.status_code, 403)

    def test_get_own_member(self):
        """Test that a member can view it's own data."""
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, 200)
        expected_user = {**TEST_MEMBER}
        del expected_user['email_verified']  # not shown to user
        for key in expected_user.keys():
            self.assertEqual(str(expected_user[key]), str(res.data[key]))

    def test_update_member(self):
        """Test that a member can edit non-admin fields of it's own data."""
        self.client.patch(ME_URL, {'first_name': 'New Name'})
        res = self.client.get(ME_URL)
        self.assertEqual(res.data['first_name'], 'New Name')
        self.assertEqual(res.data['last_name'], 'lastname')
        # TODO Check with keycloak userinfo

    def test_update_member_admin_fields_fails(self):
        """Test that a member cannot edit admin fields of it's own data."""
        res2 = self.client.put(
            ME_URL, {'membership_status': '2_provisional'})
        self.assertEqual(res2.status_code, 400)
        member = Member.objects.get(id=self.members_id)
        self.assertNotEqual(
            getattr(member, 'membership_status'), '2_provisional')


class PrivateMemberApiTestsForAdmins(TestCase):
    """Test the privatly available members API for admins."""

    def setUp(self):
        """Prepare client, extension, & micro-frontend."""
        self.client = CollectivoAPIClient()
        Member.objects.all().delete()
        user = UserInfo(
            roles=['members_admin'],
            email='test_member_1@example.com',
            first_name='firstname',
            last_name='lastname',
            is_authenticated=True,
        )
        self.client.force_authenticate(user)
        self.payload = {
            'first_name': 'firstname',
            'last_name': 'lastname',
            'email_verified': True,
            'email': 'test_member_1@example.com',
        }

    def create_members(self, n_users):
        """Create a set of members for testing."""
        for i, user in enumerate(range(n_users)):
            payload = {**self.payload, 'first_name': str(i)}
            self.client.post(MEMBERS_URL, payload)

    def test_create_members(self):
        """Test that admins can create members with access to all fields."""
        n_users_new = 5
        n_users_before = len(Member.objects.all())
        n_users_after = n_users_before + n_users_new
        self.create_members(n_users_new)
        self.assertEqual(len(Member.objects.all()), n_users_after)

    def test_update_member_admin_fields(self):
        """Test that admins can write to admin fields."""
        res1 = self.client.post(MEMBERS_URL, self.payload)
        res2 = self.client.patch(
            reverse(
                'collectivo:collectivo.members:member-detail',
                args=[res1.data['id']]),
            {'membership_status': '2_provisional'}
        )
        self.assertEqual(res2.status_code, 200)
        member = Member.objects.get(id=res1.data['id'])
        self.assertEqual(
            getattr(member, 'membership_status'), '2_provisional')

    def test_member_sorting(self):
        """Test that all member fields can be sorted."""
        n_users = 3
        self.create_members(n_users)

        res = self.client.get(MEMBERS_URL+'?orderingx=first_name')
        self.assertEqual(
            [entry['first_name'] for entry in res.data],
            ['0', '1', '2']
        )

        res = self.client.get(MEMBERS_URL+'?ordering=-first_name')
        self.assertEqual(
            [entry['first_name'] for entry in res.data],
            ['2', '1', '0']
        )

    def test_member_filtering(self):
        """Test that all member fields can be filtered."""
        n_users = 3
        self.create_members(n_users)

        res = self.client.get(MEMBERS_URL+'?first_name=1')
        self.assertEqual(
            [entry['first_name'] for entry in res.data],
            ['1']
        )

        res = self.client.get(MEMBERS_URL+'?first_name__gte=1')
        self.assertEqual(
            [entry['first_name'] for entry in res.data],
            ['1', '2']
        )

        res = self.client.get(MEMBERS_URL+'?first_name__contains=1')
        self.assertEqual(
            [entry['first_name'] for entry in res.data],
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
