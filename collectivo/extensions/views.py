"""Views of the extension manager module."""

from rest_framework.views import APIView
from rest_framework.response import Response
from keycloak import KeycloakOpenID
from django.conf import settings
from collectivo.extensions import extensions
# from .serializers import ExtensionSerializer


class ExtensionView(APIView):
    """API views of the keycloak token."""

    # def get_serializer(self, *args, **kwargs):
    #     """Return serializer for OpenAPI."""
    #     return TokenSerializer(*args, **kwargs)

    def get(self, request):
        """Return access/bearer token for given credentials."""
        # # Validate input
        # serializer = TokenSerializer(data=request.data)
        # serializer.is_valid(raise_exception=True)

        data = {
            'extensions': str([ext.name for ext in extensions.get_configs()]),
        }
        return Response(data)
