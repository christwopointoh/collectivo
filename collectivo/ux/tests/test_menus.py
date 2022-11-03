"""Test the features of the menu API."""
from django.test import TestCase
from django.urls import reverse
from ..utils import register_menuitem
from collectivo.ux.models import Menu, MenuItem
from collectivo.auth.utils import KeycloakAPIClient


EXTENSIONS_URL = reverse('collectivo:collectivo.extensions:extension-list')
MENUS_URL = reverse('collectivo:collectivo.ux:menu-list')
ITEMS_URL = reverse('collectivo:collectivo.ux:menuitem-list',
                    kwargs={'menu_id': 'main_menu'})


class PublicMenusApiTests(TestCase):
    """Test the publicly available menus API."""

    def setUp(self):
        """Prepare client, extension, & micro-frontend."""
        self.client = KeycloakAPIClient()
        self.ext_name = 'my_extension'
        self.client.post(EXTENSIONS_URL, {'name': self.ext_name})

    def test_default_menus(self):
        """Test default menus exist."""
        default_menus = ['main_menu', 'admin_menu']
        for menu in default_menus:
            self.assertTrue(Menu.objects.filter(menu_id=menu).exists())

    def test_create_menu(self):
        """Test creating menu."""
        payload = {
            'menu_id': 'my_menu',
            'extension': self.ext_name,
        }
        self.client.post(MENUS_URL, payload)
        exists = Menu.objects.filter(menu_id='my_menu').exists()
        self.assertTrue(exists)

    def test_create_menu_item(self):
        """Test creating item for a menu."""
        payload = {
            'item_id': 'my_menu_item',
            'menu_id': 'main_menu',
            'label': 'My menu item',
            'extension': self.ext_name,
        }
        self.client.post(ITEMS_URL, payload)
        exists = MenuItem.objects.filter(item_id='my_menu_item').exists()
        self.assertTrue(exists)

    def test_menu_item_correct_role(self):
        """Test menuitem should appear for user with correct role."""
        payload = {
            'item_id': 'my_menu_item',
            'menu_id': 'main_menu',
            'label': 'My menu item',
            'extension': self.ext_name,
            'required_role': 'test_role'
        }
        user = {
            'sub': 'ac4339c5-56f6-4df5-a6c8-bcdd3683a56a',
            'roles': ['test_role'],
            'email': 'test_member_1@example.com'
        }
        self.client.force_authenticate(user)
        self.client.post(ITEMS_URL, payload)
        res = self.client.get(ITEMS_URL, payload)
        items = [i['item_id'] for i in res.data]
        self.assertTrue('my_menu_item' in items)

    def test_menu_item_wrong_role(self):
        """Test menuitem should not appear for user with wrong role."""
        payload = {
            'item_id': 'my_menu_item',
            'menu_id': 'main_menu',
            'label': 'My menu item',
            'extension': self.ext_name,
            'required_role': 'wrong_role'
        }
        user = {
            'sub': 'ac4339c5-56f6-4df5-a6c8-bcdd3683a56a',
            'roles': ['test_role'],
            'email': 'test_member_1@example.com'
        }
        self.client.force_authenticate(user)
        self.client.post(ITEMS_URL, payload)
        res = self.client.get(ITEMS_URL, payload)
        items = [i['item_id'] for i in res.data]
        self.assertFalse('my_menu_item' in items)

    def test_create_menu_item_util(self):
        """Test creating item for a menu with utils."""
        payload = {
            'item_id': 'my_menu_item',
            'menu_id': 'main_menu',
            'label': 'My menu item',
            'extension': self.ext_name,
        }
        register_menuitem(**payload)
        item = MenuItem.objects.get(item_id='my_menu_item')
        self.assertTrue(item.label == 'My menu item')
        payload = {
            'item_id': 'my_menu_item',
            'menu_id': 'main_menu',
            'label': 'My menu item2',
            'extension': self.ext_name,
        }
        register_menuitem(**payload)
        item = MenuItem.objects.get(item_id='my_menu_item')
        self.assertTrue(item.label == 'My menu item2')
