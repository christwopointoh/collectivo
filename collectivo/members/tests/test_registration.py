"""Tests of the members extension."""
from django.test import TestCase
from collectivo.extensions.models import Extension
from collectivo.ux.models import MenuItem


class PublicRecipeApiTests(TestCase):
    """Test unauthenticated members API access."""

    def test_extension_exists(self):
        """Test that the extension is automatically registered."""
        exists = Extension.objects.filter(name='members').exists()
        self.assertTrue(exists)

    def test_menu_items_exist(self):
        """Test that the menu items are registered."""
        res = MenuItem.objects.filter(extension='members')
        self.assertEqual(len(res), 2)

    def test_menu_items_access(self):
        """Test that only the correct roles can view menu item."""
        # TODO Access control for menus
