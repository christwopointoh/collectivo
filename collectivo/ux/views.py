"""Views of the user experience module."""

from .menus import menus
from . import models, serializers
from rest_framework import generics, viewsets
from rest_framework.exceptions import ValidationError


class MenuItemsReadView(generics.ListAPIView):
    """API list view to receive the main menu."""

    serializer_class = serializers.MenuItemSerializer

    def get_queryset(self):
        """Get items of the main menu."""
        # TODO Show only items specific to current user
        menu_name = self.kwargs.get('menu_name')
        try:
            return menus[menu_name].items
        except KeyError:
            raise ValidationError(
                detail=f"Menu with name '{menu_name}' doesn't exist.")


class MicroFrontendViewSet(viewsets.ModelViewSet):
    """Manage micro-frontends."""

    queryset = models.MicroFrontend.objects.all()

    def get_serializer_class(self):
        """Set name to read-only except for create."""
        if self.request.method == 'POST':
            return serializers.MicroFrontendCreateSerializer
        return serializers.MicroFrontendSerializer
