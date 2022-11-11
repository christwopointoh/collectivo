"""Populate keycloak with groups and roles defined in settings."""
import logging
from collectivo.auth.manager import KeycloakManager
from django.conf import settings


logger = logging.getLogger(__name__)


def create_groups_and_roles():
    """Add groups and roles to keycloak."""
    try:
        logger.debug('Creating groups and roles')
        _create_groups_and_roles()
    except Exception as e:
        logger.debug(f'Failed to create groups and roles: {repr(e)}')


def _create_groups_and_roles():
    """Add groups and roles to keycloak."""
    keycloak_admin = KeycloakManager().keycloak_admin

    # Get groups and roles from settings
    groups_and_roles = settings.COLLECTIVO['auth_groups_and_roles']

    # Create groups
    for group_name in groups_and_roles.keys():
        keycloak_admin.create_group(
            payload={"name": group_name},
            skip_exists=True,
        )

    # Create roles
    for role_names in groups_and_roles.values():
        for role_name in role_names:
            keycloak_admin.create_realm_role(
                payload={'name': role_name},
                skip_exists=True
            )

    # Add roles to groups
    for group_name, role_names in groups_and_roles.items():
        group_id = keycloak_admin.get_group_by_path(f'/{group_name}')['id']
        for role_name in role_names:
            role_id = keycloak_admin.get_realm_role(
                role_name=role_name
            )['id']
            keycloak_admin.assign_group_realm_roles(
                group_id=group_id,
                roles=[{'name': role_name, 'id': role_id}]
            )
