"""Middlewares of the authentication module."""
from django.conf import settings
from django.http.response import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from keycloak import KeycloakOpenID
from rest_framework.exceptions import AuthenticationFailed


class KeycloakMiddleware(MiddlewareMixin):
    """KeyCloak Middleware for authentication and authorization."""

    def __init__(self, get_response):
        """One-time initialization of middleware."""
        self.get_response = get_response  # Django default setting
        self.config = settings.KEYCLOAK_CONFIG

        # Keycloak OpenID client
        self.keycloak = KeycloakOpenID(
            server_url=self.config["SERVER_URL"],
            realm_name=self.config["REALM_NAME"],
            client_id=self.config["CLIENT_ID"],
            client_secret_key=self.config["CLIENT_SECRET_KEY"],
        )

    def __call__(self, request):
        """Handle default requests."""
        return self.get_response(request)

    def process_view(self, request, view_func, view_args, view_kwargs):
        """Check for authentication and try to get userinfo from keycloak."""
        # Skip authentication if userinfo is already given (e.g. by a test)
        if hasattr(request, 'userinfo'):
            return None

        # Define unauthenticated request
        request.userinfo = None

        # Return unauthenticated request if no authorization is found
        if "HTTP_AUTHORIZATION" not in request.META:
            return None

        # Retrieve token and userinfo or return failure message
        try:
            auth = request.META.get("HTTP_AUTHORIZATION").split()
            access_token = auth[1] if len(auth) == 2 else auth[0]
            request.userinfo = self.keycloak.userinfo(access_token)
        except Exception:
            return JsonResponse(
                {"detail": AuthenticationFailed.default_detail},
                status=AuthenticationFailed.status_code,
            )

        # Return authenticated request
        return None
