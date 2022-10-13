"""Views of the menus module."""

from .menus import menus
from .serializers import MenuItemSerializer
from rest_framework import generics
from rest_framework.exceptions import ValidationError


class MenuItemsReadView(generics.ListAPIView):
    """API list view to receive the main menu."""

    serializer_class = MenuItemSerializer

    def get_queryset(self):
        """Get items of the main menu."""
        # TODO Show only items specific to current user
        menu_name = self.kwargs.get('menu_name')
        try:
            return menus[menu_name].items
        except KeyError:
            raise ValidationError(
                detail=f"Menu with name '{menu_name}' doesn't exist.")
