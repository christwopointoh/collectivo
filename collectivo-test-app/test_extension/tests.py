"""Tests of the test_extension extension."""
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from collectivo.menus.models import MenuItem
from collectivo.extensions.models import Extension


EXTENSIONS_URL = reverse('collectivo:collectivo.extensions:extension-list')
MENUS_URL = reverse('collectivo:collectivo.menus:menu-list')
ITEMS_URL = reverse('collectivo:collectivo.menus:menuitem-list',
                    kwargs={'menu_id': 'main_menu'})


class PublicMenusApiTests(TestCase):
    """Test the publicly available menus API."""

    def setUp(self):
        """Prepare client."""
        self.client = APIClient()

    def test_extension_exists(self):
        """Test extension exists."""
        extensions = Extension.objects.filter(name='test_extension')
        self.assertTrue(extensions.exists())

    def test_default_menus(self):
        """Test menu items exist."""
        items = MenuItem.objects.filter(extension='test_extension')
        self.assertEqual(len(items), 3)
