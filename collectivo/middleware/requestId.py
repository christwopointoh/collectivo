# file collectivo.middleware.requestId.py

# Local Library
import uuid

class AddRequestId():

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.META["X-Request-ID"] = str(uuid.uuid4())
        response = self.get_response(request)
        response["X-Request-ID"] = request.META["X-Request-ID"]
        return response