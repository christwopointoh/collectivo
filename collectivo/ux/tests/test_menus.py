"""Test the features of the menu API."""

from django.test import TestCase, SimpleTestCase
from django.urls import reverse

from rest_framework.test import APIClient
from collectivo.ux.menus import Menu, MenuItem, menus, main_menu
from collectivo.ux.serializers import MenuItemSerializer


def create_menu_item():
    """Return a menu item."""
    return MenuItem(
        display='This is a menu item',
        path='static/tests/hello_world',
    )


class MenuCreationTests(SimpleTestCase):
    """Test features of the menus module."""

    def testCreateMenu(self):
        """Test that new menu is registered in menus."""
        mymenu = Menu('mymenu')
        self.assertIn(('mymenu', mymenu), menus.items())

    def testCreateMenuItem(self):
        """Test that items can be added to menus."""
        mymenu = Menu('mymenu')
        myitem = create_menu_item()
        mymenu.add_item(myitem)
        self.assertIn(myitem, mymenu.items)

    # TODO Test Subitems


class PublicMenuApiTests(TestCase):
    """Test public features of the menus API."""

    def setUp(self):
        """Set up the test client."""
        self.client = APIClient()
        myitem = create_menu_item()
        main_menu.add_item(myitem)

    def testGetMenuItems(self):
        """Test getting items of a menu."""
        url = reverse(
            'collectivo:collectivo.ux:menu',
            kwargs={'menu_name': 'main_menu'}
        )
        res = self.client.get(url)
        menu_items = MenuItemSerializer(main_menu.items, many=True).data
        self.assertEqual(menu_items, res.data)
