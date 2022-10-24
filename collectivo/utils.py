"""Utility functions of the collectivo package."""

from django.test import RequestFactory
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet


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
