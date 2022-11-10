"""Views of the dashboard extension."""
from rest_framework import viewsets, mixins


class DasboardTileViewSet(
        mixins.CreateModelMixin,
        mixins.RetrieveModelMixin,
        mixins.UpdateModelMixin,
        viewsets.GenericViewSet
        ):
    """Manage dashboard tiles."""

    pass
