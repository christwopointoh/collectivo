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

    def authentication_failed(self):
        """Return JSON saying that authentication has failed."""
        return JsonResponse(
            {"detail": AuthenticationFailed.default_detail},
            status=AuthenticationFailed.status_code,
        )

    def not_authenticated(self):
        """Return JSON saying that user is not authorized."""
        return JsonResponse(
            {"detail": NotAuthenticated.default_detail},
            status=NotAuthenticated.status_code,
        )

    def get_token(self, request):
        """Get token for passed authorization data."""
        # Check for authorization data in header
        if "HTTP_AUTHORIZATION" not in request.META:
            request.is_authenticated = False
            return self.keycloak.token("anon", "anon")['access_token']
        else:
            # Read out token from header
            request.is_authenticated = True
            auth_header = request.META.get("HTTP_AUTHORIZATION").split()
            return auth_header[1] if len(auth_header) == 2 else auth_header[0]

    def process_view(self, request, view_func, view_args, view_kwargs):
        """Check if user is authorized for given view."""
        try:
            print(request.method)  # GET
            print(request.path)  # /api/extensions/v1/extensions/
            print(view_func.cls.__name__)  # ExtensionViewSet
            #print(dir(view_func))
            #print(dir(view_func.cls))
            #print(dir(view_func.view_class))
            #print(view_args)
            #print(view_kwargs)
            resource = 'test_resource'
            scope = 'view'
            uma = self.keycloak.has_uma_access(
                self.get_token(request),
                f"{resource}#{scope}"
            )
        except KeycloakAuthenticationError:
            return None
            request.is_authenticated = False
            return self.authentication_failed()

        return None if uma.is_authorized else self.not_authenticated()


