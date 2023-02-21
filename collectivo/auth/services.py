"""Manager class to connect collectivo to an authentication service."""
from keycloak import KeycloakAdmin, KeycloakOpenID
from keycloak.exceptions import KeycloakPutError, KeycloakDeleteError
from collectivo.auth.exceptions import AuthDeleteError
from rest_framework.exceptions import ParseError
from django.conf import settings
from collectivo.utils import get_object_from_settings
from dataclasses import dataclass
from uuid import UUID


@dataclass
class AuthUser:
    """Representation for users of the authentication service."""

    user_id: UUID
    email: str
    first_name: str
    last_name: str


class AuthService:
    """Representation of the authentication service."""

    def __init__(self):
        """Initialize auth manager as defined in settings."""
        self._manager = get_object_from_settings("auth.service")()

    def get_user_id(self, email: str) -> UUID:
        """Return user id from auth service."""
        return self._manager.get_user_id(email)

    def get_user(self, user_id: UUID) -> AuthUser:
        """Return user from auth service."""
        return self._manager.get_user(user_id)

    def create_user(
        self,
        first_name: str,
        last_name: str,
        email: str,
        email_verified: bool = False,
    ) -> str:
        """Create user in auth service. Returns user id."""
        return self._manager.create_user(
            first_name, last_name, email, email_verified
        )

    def set_user_password(
        self, user_id: UUID, password: str, temporary: bool = True
    ) -> None:
        """Update user password in auth service."""
        self._manager.set_user_password(user_id, password, temporary)

    def delete_user(self, user_id: UUID) -> None:
        """Delete user from auth service."""
        self._manager.delete_user(user_id)

    def __getattr__(self, name):
        """Return attribute from auth manager."""
        return getattr(self._manager, name)


class KeycloakAuthService:
    """Keycloak authentication service."""

    def __init__(self):
        """Initialize keycloak admin."""
        config = settings.KEYCLOAK
        self.admin = KeycloakAdmin(
            server_url=config["SERVER_URL"],
            realm_name=config["REALM_NAME"],
            client_id=config["CLIENT_ID"],
            client_secret_key=config["CLIENT_SECRET_KEY"],
            verify=True,
        )
        self.openid = KeycloakOpenID(
            server_url=config["SERVER_URL"],
            client_id=config["REALM_NAME"],
            realm_name=config["CLIENT_ID"],
            client_secret_key=config["CLIENT_SECRET_KEY"],
        )

    def get_user_fields(self):
        """Return attributes of the user model."""
        return ("first_name", "last_name", "email")

    def get_user(self, user_id) -> AuthUser:
        """Return user from keycloak."""
        user_rep = self.admin.get_user(user_id)
        return AuthUser(
            user_id=user_id,
            email=user_rep["email"],
            first_name=user_rep["firstName"],
            last_name=user_rep["lastName"],
        )

    def get_user_id(self, email):
        """Return user id from keycloak."""
        return self.admin.get_user_id(email)

    def set_user_password(
        self, user_id: UUID, password: str, temporary: bool = True
    ) -> None:
        """Update user password in keycloak."""
        self.admin.set_user_password(user_id, password, temporary=temporary)

    def delete_user(self, user_id):
        """Delete a keycloak user."""
        try:
            self.admin.delete_user(user_id)
        except KeycloakDeleteError as e:
            raise AuthDeleteError(e.error_message)

    def __getattr__(self, name):
        """Return attribute from auth manager."""
        return getattr(self.admin, name)

    def create_user(
        self,
        first_name,
        last_name,
        email,
        email_verified=False,
        exist_ok=False,
    ):
        """Create a keycloak user."""
        payload = {
            "firstName": first_name,
            "lastName": last_name,
            "email": email,
            "username": email,
            "enabled": True,
            "emailVerified": email_verified,
        }
        try:
            user = self.admin.create_user(payload, exist_ok=exist_ok)
        except Exception as e:
            raise ParseError(f"Could not create user: {e}")
        return user

    def update_user(
        self,
        user_id,
        first_name=None,
        last_name=None,
        email=None,
        email_verified=None,
    ):
        """Update a keycloak user."""
        payload = {
            "firstName": first_name,
            "lastName": last_name,
            "email": email,
            "emailVerified": email_verified,
        }
        payload = {k: v for k, v in payload.items() if v is not None}
        try:
            self.admin.update_user(user_id=user_id, payload=payload)
        except KeycloakPutError as e:
            raise ParseError(f"Could not update user {user_id}: {e}")

    def add_user_to_group(self, user_id, group_name):
        """Add a user to a keycloak group."""
        group_id = self.get_group_by_path(f"/{group_name}")["id"]
        self.group_user_add(user_id, group_id)

    def remove_user_from_group(self, user_id, group_name):
        """Remove a user from an authorization group."""
        group_id = self.get_group_by_path(f"/{group_name}")["id"]
        self.group_user_remove(user_id, group_id)
