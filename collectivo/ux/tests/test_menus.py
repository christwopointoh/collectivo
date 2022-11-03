"""Test the features of the menu API."""
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from collectivo.ux.models import Menu, MenuItem
from ..utils import register_menuitem


EXTENSIONS_URL = reverse('collectivo:collectivo.extensions:extension-list')
MENUS_URL = reverse('collectivo:collectivo.ux:menu-list')
ITEMS_URL = reverse('collectivo:collectivo.ux:menuitem-list',
                    kwargs={'menu_id': 'main_menu'})


class PublicMenusApiTests(TestCase):
    """Test the publicly available menus API."""

    def setUp(self):
        """Prepare client, extension, & micro-frontend."""
        self.client = APIClient()
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
