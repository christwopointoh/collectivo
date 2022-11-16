"""Populate auth service with groups and roles."""
import logging
from collectivo.utils import get_auth_manager
from django.conf import settings


logger = logging.getLogger(__name__)


def create_groups_and_roles():
    """Add groups and roles to auth service."""
    logger.debug('Creating groups and roles')
    auth_manager = get_auth_manager()

    # Get groups and roles from settings
    groups_and_roles = settings.COLLECTIVO['auth_groups_and_roles']

    # Create groups
    for group_name in groups_and_roles.keys():
        auth_manager.create_group(
            payload={"name": group_name},
            skip_exists=True,
        )

    # Create roles
    for role_names in groups_and_roles.values():
        for role_name in role_names:
            auth_manager.create_realm_role(
                payload={'name': role_name},
                skip_exists=True
            )

    # Add roles to groups
    for group_name, role_names in groups_and_roles.items():
        group_id = auth_manager.get_group_by_path(f'/{group_name}')['id']
        for role_name in role_names:
            role_id = auth_manager.get_realm_role(
                role_name=role_name
            )['id']
            auth_manager.assign_group_realm_roles(
                group_id=group_id,
                roles=[{'name': role_name, 'id': role_id}]
            )
