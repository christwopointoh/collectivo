"""A manager for keycloak users and permissions."""
from keycloak import KeycloakAdmin
from django.conf import settings


class KeycloakManager:
    """Keycloak admin connection."""

    def __init__(self):
        """Initialize keycloak admin manager."""
        config = settings.COLLECTIVO['auth_keycloak_config']
        self.keycloak_admin = KeycloakAdmin(
            server_url=config["SERVER_URL"],
            realm_name=config["REALM_NAME"],
            client_id=config["CLIENT_ID"],
            client_secret_key=config["CLIENT_SECRET_KEY"],
            verify=True
        )


keycloak_admin = KeycloakManager().keycloak_admin


def add_user_to_group(user_id, group_name):
    """Add a user to an authorization group."""
    group_id = keycloak_admin.get_group_by_path(f'/{group_name}')['id']
    keycloak_admin.group_user_add(user_id, group_id)


def remove_user_from_group(user_id, group_name):
    """Remove a user from an authorization group."""
    group_id = keycloak_admin.get_group_by_path(f'/{group_name}')['id']
    keycloak_admin.group_user_remove(user_id, group_id)
