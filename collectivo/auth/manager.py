"""A manager for keycloak users and permissions."""
from keycloak import KeycloakAdmin
from django.conf import settings


class KeycloakManager:
    """Keycloak admin connection."""

    def __init__(self):
        """Initialize keycloak admin manager."""
        config = settings.KEYCLOAK_CONFIG
        self.keycloak_admin = KeycloakAdmin(
            server_url=config["SERVER_URL"],
            realm_name=config["REALM_NAME"],
            client_id=config["CLIENT_ID"],
            client_secret_key=config["CLIENT_SECRET_KEY"],
            verify=True
        )
