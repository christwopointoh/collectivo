"""
Middleware to log `*/api/*` requests and responses.
"""
import socket
import time
import json
import logging

request_logger = logging.getLogger(__name__)

class RequestLogMiddleware:
    """Request Logging Middleware."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()
        log_data = {
            "remote_address": request.META["REMOTE_ADDR"],
            "server_hostname": socket.gethostname(),
            "request_method": request.method,
            "request_path": request.get_full_path(),
        }

        # Only logging "*/api/*" patterns
        if "/api/" in str(request.get_full_path()):
            req_body = json.loads(request.body.decode("utf-8")) if request.body else {}
            log_data["request_body"] = req_body

        # request passes on to controller
        response = self.get_response(request)

        log_data["status_code"] = response.status_code

        if request.userinfo is not None:
            log_data["user"] = request.userinfo.user_id

        if request.META["X-Request-ID"] is not None:
            log_data["request_id"] = request.META["X-Request-ID"]

        # add runtime to our log_data
        log_data["run_time"] = time.time() - start_time
        request_logger.info(msg=log_data)

        return response

    # Log unhandled exceptions as well
    def process_exception(self, request, exception):
        try:
            raise exception
        except Exception as e:
            request_logger.exception("Unhandled Exception: " + str(e))
        return exception
