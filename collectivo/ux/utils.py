"""Utility functions of the user experience module."""
from collectivo.ux import views
from collectivo.utils import request
from rest_framework.response import Response


def register_viewset(viewset, pk, **kwargs) -> Response:
    """Register an internal extension."""
    get = request(viewset, 'retrieve', kwargs, pk=pk)
    if get.status_code == 200:
        return request(viewset, 'update', kwargs, pk=pk)
    else:
        return request(viewset, 'create', kwargs)


def register_menu(**attrs):
    """Register a menu."""
    pk = attrs['menu_id']
    return register_viewset(views.MenuViewSet, pk, **attrs)


def register_menuitem(**attrs):
    """Register a menu item."""
    pk = attrs['item_id']
    return register_viewset(views.MenuItemViewSet, pk, **attrs)
