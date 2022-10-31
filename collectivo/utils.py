"""Utility functions of the collectivo package."""

from django.test import RequestFactory
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.routers import Route, SimpleRouter


def request(viewset: ViewSet, command='create', payload=None,
            **kwargs) -> Response:
    """Make an internal http request to a DRF Viewset."""
    rf = RequestFactory()
    drf_to_http = {
        'create': 'post',
        'update': 'put',
        'retrieve': 'get',
        'list': 'get'
    }

    method = drf_to_http[command]

    request = getattr(rf, method)(
        None, payload, content_type="application/json")

    return viewset.as_view({method: command})(request, **kwargs)


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
