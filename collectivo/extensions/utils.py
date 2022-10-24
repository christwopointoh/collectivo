"""Utility functions of the extensions module."""

from collectivo.extensions.views import ExtensionViewSet
from collectivo.utils import request
from rest_framework.response import Response


def register_extension(name: str, **kwargs) -> Response:
    """Register an internal extension."""
    get = request(ExtensionViewSet, 'retrieve', kwargs, pk=name)
    if get.status_code == 200:
        return request(ExtensionViewSet, 'update', kwargs, pk=name)
    else:
        kwargs['name'] = name
        return request(ExtensionViewSet, 'create', kwargs)
