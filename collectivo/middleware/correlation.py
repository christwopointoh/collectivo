# file collectivo.middleware.correlation.py

# Standard Library
import logging

# Local Library
from threading import local
import uuid

class Correlation():

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.META["X-Correlation-ID"] = str(uuid.uuid4())
        response = self.get_response(request)
        response["X-Correlation-ID"] = request.META["X-Correlation-ID"]
        return response