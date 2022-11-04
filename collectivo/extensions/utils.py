"""Utility functions of the extensions module."""
from collectivo.extensions.views import ExtensionViewSet
from collectivo.utils import request
from rest_framework.response import Response


def register_extension(name: str, **kwargs) -> Response:
    """Register an internal extension."""
    # TODO Delete old stuff first?
    # get = request(ExtensionViewSet, 'retrieve', kwargs, pk=name)
    # if get.status_code == 200:
    kwargs['name'] = name
    request(ExtensionViewSet, 'destroy', kwargs, pk=name)
    return request(ExtensionViewSet, 'create', kwargs, pk=name)
    # else:
    #     kwargs['name'] = name
    #     return request(ExtensionViewSet, 'create', kwargs)
