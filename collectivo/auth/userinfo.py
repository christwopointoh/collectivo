"""Userinfo class of the authentication module."""
import logging


logger = logging.getLogger(__name__)


class UserInfo:
    """Class for storing information about a user."""

    def __init__(self,
                 user_id: str = None,
                 email: str = None,
                 email_verified: bool = False,
                 is_authenticated: bool = False,
                 first_name: str = None,
                 last_name: str = None,
                 roles: list[str] = None):
        """Initialize object."""
        self.user_id = user_id
        self.email = email
        self.email_verified = email_verified
        self.is_authenticated = is_authenticated
        self.first_name = first_name
        self.last_name = last_name
        self.roles = roles if roles is not None else []

    def has_role(self, role: str) -> bool:
        """Check if user has role."""
        try:
            return role in self.roles
        except Exception as e:
            logger.debug(
                f"Error while trying to check if user"
                f"{self.id} has role {role}: {repr(e)}"
            )
            return False
