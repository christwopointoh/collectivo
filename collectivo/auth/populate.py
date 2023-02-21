"""Populate auth service with groups and roles."""
import logging
from collectivo.auth.models import AuthService


logger = logging.getLogger(__name__)


def create_groups_and_roles():
    """Add groups and roles to auth service."""
    logger.debug("Creating roles")
    auth_service = AuthService()

    # TODO Get automatically from extensions
    roles = [
        "superuser",
        "members_user",
        "members_admin",
        "shifts_user",
        "shifts_admin",
    ]

    # Create roles
    for role in roles:
        auth_service.create_realm_role(
            payload={"name": role}, skip_exists=True
        )
