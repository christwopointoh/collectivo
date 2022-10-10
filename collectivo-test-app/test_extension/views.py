"""Views of the test_extension extension."""

from rest_framework.views import APIView
from rest_framework.response import Response
from collectivo.version import __version__


class TestView(APIView):
    """A view of the test_extension extension."""

    def get(self, request):
        """Return success."""
        data = {
            'message': 'Hi! I am the test_extension :)',
        }
        return Response(data)
