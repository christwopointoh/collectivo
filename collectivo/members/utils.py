"""Utility functions of the dashboard module."""
from collectivo.utils import register_viewset
from .views import MemberTagViewSet


def register_tag(**payload):
    """Register a dashboard tile."""
    pk = payload['tag_id']
    return register_viewset(MemberTagViewSet, pk, payload=payload)
