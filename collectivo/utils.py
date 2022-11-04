"""Utility functions of the collectivo package."""
from django.test import RequestFactory
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet


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

    return viewset.as_view({method: command})(request, **kwargs)
