"""Middlewares of the authentication module."""
from django.conf import settings
from django.http.response import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from keycloak import KeycloakOpenID
from keycloak.exceptions import (
    KeycloakAuthenticationError
)
from rest_framework.exceptions import (
    AuthenticationFailed,
    NotAuthenticated,
)


class KeycloakMiddleware(MiddlewareMixin):
    """KeyCloak Middleware for Authentication and Authorization."""

    def __init__(self, get_response):
        """One-time initialization of middleware."""
        self.get_response = get_response  # Django default setting
        self.config = settings.KEYCLOAK_CONFIG

        # Create Keycloak OpenID client
        self.keycloak = KeycloakOpenID(
            server_url=self.config["SERVER_URL"],
            realm_name=self.config["REALM_NAME"],
            client_id=self.config["CLIENT_ID"],
            client_secret_key=self.config["CLIENT_SECRET_KEY"],
        )

    def __call__(self, request):
        """Handle requests.."""
        return self.get_response(request)  # Django default setting

    def process_view(self, request, view_func, view_args, view_kwargs):
        """Validate keycloak token."""
        # Check for authorization data in header
        # Return error to client if it is missing
        if "HTTP_AUTHORIZATION" not in request.META:
            # return JsonResponse(
            #     {
            #         "detail": "Authentication credentials not provided.",
            #     },
            #     status=NotAuthenticated.status_code,
            # )
            pass

        else:

            # Read out token from header
            auth_header = request.META.get("HTTP_AUTHORIZATION").split()
            token = auth_header[1] if len(auth_header) == 2 else auth_header[0]

            try:
                parsed_token = self.keycloak.introspect(token)
                if parsed_token["active"]:
                    request.is_authenticated = True
            except KeycloakAuthenticationError:
                return JsonResponse(
                    {"detail": AuthenticationFailed.default_detail},
                    status=AuthenticationFailed.status_code,
                )

            # TODO Get user from token
            # user, _ = User.objects.get_or_create(
            #     username=parsed_token['preferred_username'],
            #     first_name=parsed_token["given_name"],
            #     last_name=parsed_token["family_name"]
            # )

        # TODO Check if user has permissions to access this view
        has_permissions = True
        if has_permissions:
            return None
        else:
            # TODO Which is the correct error message here?
            return JsonResponse(
                {
                    "detail": NotAuthenticated.default_detail,
                },
                status=NotAuthenticated.status_code,
            )
