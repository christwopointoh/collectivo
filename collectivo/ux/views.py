"""Views of the user experience module."""

from . import models, serializers
from rest_framework import viewsets


class MicroFrontendViewSet(viewsets.ModelViewSet):
    """Manage micro-frontends."""

    queryset = models.MicroFrontend.objects.all()

    def get_serializer_class(self):
        """Set name to read-only except for create."""
        if self.request.method == 'POST':
            return serializers.MicroFrontendCreateSerializer
        return serializers.MicroFrontendSerializer


class MenuViewSet(viewsets.ModelViewSet):
    """Manage menus."""

    queryset = models.Menu.objects.all()

    def get_serializer_class(self):
        """Set name to read-only except for create."""
        if self.request.method == 'POST':
            return serializers.MenuCreateSerializer
        return serializers.MenuSerializer


class MenuItemViewSet(viewsets.ModelViewSet):
    """Manage menu-items."""

    queryset = models.MenuItem.objects.all()

    def get_serializer_class(self):
        """Set name to read-only except for create."""
        if self.request.method == 'POST':
            return serializers.MenuItemCreateSerializer
        return serializers.MenuItemSerializer
