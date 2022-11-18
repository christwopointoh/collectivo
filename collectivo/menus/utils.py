"""Utility functions of the user experience module."""
from collectivo.menus import views
from collectivo.utils import register_viewset


def register_menu(**attrs):
    """Register a menu."""
    pk = attrs['menu_id']
    return register_viewset(views.MenuViewSet, pk, **attrs)


def register_menuitem(**attrs):
    """Register a menu item."""
    pk = attrs['item_id']
    return register_viewset(views.MenuItemViewSet, pk, **attrs)
