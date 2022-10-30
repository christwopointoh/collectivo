"""Views of the collectivo core."""
from rest_framework.views import APIView
from rest_framework.response import Response
from collectivo.version import __version__


class VersionView(APIView):
    """API views of the project version."""

    def get(self, request):
        """Return the current version of the project."""
        data = {
            'version': __version__,
        }
        return Response(data)
