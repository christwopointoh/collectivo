"""Utility functions of the user experience module."""
from collectivo.ux import views
from collectivo.utils import request


def register_microfrontend(name, **kwargs):
    """Register an internal microfrontend."""
    request(views.MicroFrontendViewSet, 'create', {'name': name, **kwargs})


def register_menu(name, **kwargs):
    """Register an internal microfrontend."""
    request(views.MenuViewSet, 'create', {'name': name, **kwargs})


def register_menuitem(name, **kwargs):
    """Register an internal microfrontend."""
    request(views.MenuItemViewSet, 'create', {'name': name, **kwargs})
