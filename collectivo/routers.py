"""Routers of the collectivo package."""
from rest_framework.routers import Route, SimpleRouter


class DirectDetailRouter(SimpleRouter):
    """A DRF router for detail views that don't need a primary key."""

    routes = [
        Route(
            url=r'^{prefix}$',
            mapping={
                'get': 'retrieve',
                'post': 'create',
                'patch': 'partial_update',
                'put': 'update'
            },
            name='{basename}',
            detail=False,
            initkwargs={'suffix': 'Instance'}
        ),
    ]
