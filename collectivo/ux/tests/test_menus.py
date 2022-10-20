"""Test the features of the menu API."""
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from collectivo.ux.models import Menu, MenuItem


EXTENSIONS_URL = reverse('collectivo:collectivo.extensions:extension-list')
MENUS_URL = reverse('collectivo:collectivo.ux:menu-list')
ITEMS_URL = reverse('collectivo:collectivo.ux:menuitem-list')


class PublicMenusApiTests(TestCase):
    """Test the publicly available menus API."""

    def setUp(self):
        """Prepare client, extension, & micro-frontend."""
        self.client = APIClient()
        self.ext_name = 'my_extension'
        self.client.post(EXTENSIONS_URL, {'name': self.ext_name})

    def test_default_menus(self):
        """Test default menus exist."""
        default_menus = ['main_menu']
        for menu in default_menus:
            self.assertTrue(Menu.objects.filter(name=menu).exists())

    def test_create_menu(self):
        """Test creating menu."""
        payload = {
            'name': 'my_menu',
            'extension': self.ext_name,
        }
        self.client.post(MENUS_URL, payload)
        exists = Menu.objects.filter(name='my_menu').exists()
        self.assertTrue(exists)

    def test_create_menu_item(self):
        """Test creating item for a menu."""
        payload = {
            'name': 'my_menu_item',
            'label': 'My menu item',
            'menu': 'main_menu',
            'extension': self.ext_name,
        }
        self.client.post(ITEMS_URL, payload)
        exists = MenuItem.objects.filter(name='my_menu_item').exists()
        self.assertTrue(exists)
