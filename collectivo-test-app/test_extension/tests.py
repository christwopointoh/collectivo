"""Tests of the test_extension extension."""
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from collectivo.menus.models import MenuItem
from collectivo.members.models import Member
from collectivo.extensions.models import Extension
from collectivo.utils import get_auth_manager
from .populate import members, users

EXTENSIONS_URL = reverse('collectivo:collectivo.extensions:extension-list')
MENUS_URL = reverse('collectivo:collectivo.menus:menu-list')
ITEMS_URL = reverse('collectivo:collectivo.menus:menuitem-list',
                    kwargs={'menu_id': 'main_menu'})


class TestExtensionRegistrationTests(TestCase):
    """Test the publicly available menus API."""

    def setUp(self):
        """Prepare client."""
        self.client = APIClient()
        self.auth_manager = get_auth_manager()

    def test_extension_exists(self):
        """Test extension exists."""
        extensions = Extension.objects.filter(name='test_extension')
        self.assertTrue(extensions.exists())

    def test_default_menus(self):
        """Test menu items exist."""
        items = MenuItem.objects.filter(extension='test_extension')
        self.assertEqual(len(items), 3)

    def test_test_users_exist(self):
        """Test that test users exist."""
        for user in users:
            user_id = self.auth_manager.get_user_id(user['email'])
            groups = self.auth_manager.get_user_groups(user_id)
            groups = [group['name'] for group in groups]

            if user in members:
                self.assertTrue(
                    Member.objects.filter(email=user['email']).exists())
                self.assertTrue('members' in groups)
