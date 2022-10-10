"""Views of the test_extension extension."""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import HttpResponse, HttpResponseNotFound


class TestView(APIView):
    """A view of the test_extension extension."""

    def get(self, request):
        """Return success."""
        data = {
            'message': 'Hi! I am the test_extension :)',
        }
        return Response(data)


@api_view(['GET'])
def fetch_ux(request):
    """Get javascript file."""
    file_location = 'test_extension/ux/bundle.js'

    try:
        file = open(file_location, 'r')

        # Sending response
        response = HttpResponse(file, content_type='application/javascript')
        response['Content-Disposition'] = 'attachment; filename="bundle.js"'

    except IOError:
        response = HttpResponseNotFound('<h1>File not exist</h1>')

    return response
