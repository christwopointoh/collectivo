"""Views of the menus extension."""
import logging

from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated

from collectivo.utils.mixins import RetrieveModelByExtAndNameMixin
from collectivo.utils.permissions import IsSuperuser

from . import models, serializers

logger = logging.getLogger(__name__)


class MenuViewSet(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    RetrieveModelByExtAndNameMixin,
):
    """Manage menus.

    Menus are not retrieved by ID, but by extension and menu name.
    Requires authentication to read (GET), and the role 'superuser' to write.
    """

    queryset = models.Menu.objects.all()
    serializer_class = serializers.MenuSerializer

    def get_permissions(self):
        """Set permissions for this viewset."""
        if self.request.method == "GET":
            return [IsAuthenticated()]
        return [IsSuperuser()]


class MenuItemViewSet(viewsets.ModelViewSet):
    """Manage menu-items. Requires the role 'superuser'."""

    queryset = models.MenuItem.objects.all()
    serializer_class = serializers.MenuItemSerializer
    permission_classes = [IsSuperuser]
