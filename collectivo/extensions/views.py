"""Views of the extension manager module."""

from rest_framework.views import APIView
from rest_framework.response import Response
from collectivo.extensions import extensions


class ExtensionView(APIView):
    """API views of the keycloak token."""

    def get(self, request):
        """Return access/bearer token for given credentials."""
        data = {
            'extensions': str([ext.name for ext in extensions.get_configs()]),
        }
        return Response(data)
