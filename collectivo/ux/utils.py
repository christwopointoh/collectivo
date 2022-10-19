"""Utility functions of the user experience module."""
from collectivo.ux.views import MicroFrontendViewSet
from collectivo.utils import request


def register_microfrontend(name, **kwargs):
    """Register an internal microfrontend."""
    request(MicroFrontendViewSet, 'create', {'name': name, **kwargs})
