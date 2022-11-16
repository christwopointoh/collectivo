"""Utility functions of the dashboard module."""
from collectivo.utils import register_viewset
from .views import DashboardTileViewSet


def register_tile(**attrs):
    """Register a dashboard tile."""
    pk = attrs['tile_id']
    return register_viewset(DashboardTileViewSet, pk, **attrs)
