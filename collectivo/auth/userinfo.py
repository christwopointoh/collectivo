"""Userinfo class of the authentication module."""
from dataclasses import dataclass, field
import logging


logger = logging.getLogger(__name__)


@dataclass
class UserInfo:
    """Class for storing information about a user."""

    user_id: str = None
    email: str = None
    email_verified: bool = False
    is_authenticated: bool = False
    first_name: str = None
    last_name: str = None
    roles: list[str] = field(default_factory=list)

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
