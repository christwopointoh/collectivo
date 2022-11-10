"""Utility functions of the collectivo package."""
from django.test import RequestFactory
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from collectivo.auth.userinfo import UserInfo
import logging


logger = logging.getLogger(__name__)


# https://docs.djangoproject.com/en/4.1/ref/models/querysets/#field-lookups
filter_lookups = [
    'exact', 'iexact', 'contains', 'icontains', 'in', 'gt', 'gte',
    'lt', 'lte', 'startswith', 'istartswith', 'endswith', 'iendswith',
    'range',  # 'date', 'year', 'iso_year', 'month', 'day', 'week',
    # 'week_day', 'iso_week_day', 'quarter', 'time', 'hour', 'minute',
    # 'second', 'isnull', 'regex', 'iregex',
]


def request(viewset: ViewSet, command='create', payload=None,
            **kwargs) -> Response:
    """Make an internal http request to a DRF Viewset."""
    rf = RequestFactory()
    drf_to_http = {
        'create': 'post',
        'update': 'put',
        'retrieve': 'get',
        'list': 'get',
        'destroy': 'delete',
    }

    method = drf_to_http[command]

    request = getattr(rf, method)(
        None, payload, content_type="application/json")

    request.userinfo = UserInfo(roles=['collectivo_admin'])

    response = viewset.as_view({method: command})(request, **kwargs)

    return response


def register_viewset(viewset, pk, **kwargs) -> Response:
    """Register a viewset."""
    get = request(viewset, 'retrieve', kwargs, pk=pk)
    if get.status_code == 200:
        response = request(viewset, 'update', kwargs, pk=pk)
    else:
        response = request(viewset, 'create', kwargs)
    if response.status_code not in [200, 201]:
        response.render()
        logger.debug(
            f"Could not register viewset '{viewset}': {response.content}")
    return response
