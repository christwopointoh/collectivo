"""Populate keycloak with data for testing purposes."""
from collectivo.auth.manager import KeycloakManager
from keycloak.exceptions import KeycloakPostError


def populate_keycloak_with_test_data():
    """Add users, groups, and roles to keycloak."""
    keycloak_admin = KeycloakManager().keycloak_admin

    # Define groups and roles
    groups_and_roles = {
        'superusers': ['collectivo_admin', 'members_admin'],
        'members': ['members_user']
    }

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

    # Add users
    users = [
        {
            "email": "test_superuser_1@example.com",
            "username": "test_superuser_1",
            "enabled": True,
            "firstName": "Example",
            "lastName": "Example",
            "emailVerified": True
        },
        {
            "email": "test_member_1@example.com",
            "username": "test_member_1",
            "enabled": True,
            "firstName": "Example",
            "lastName": "Example",
            "emailVerified": True
        },
        {
            "email": "test_member_2@example.com",
            "username": "test_member_2",
            "enabled": True,
            "firstName": "Example",
            "lastName": "Example",
            "emailVerified": True
        },
        {
            "email": "test_user_not_verified@example.com",
            "username": "test_user_not_verified",
            "enabled": True,
            "firstName": "Example",
            "lastName": "Example",
            "emailVerified": False
        },
        {
            "email": "test_user_not_member@example.com",
            "username": "test_user_not_member",
            "enabled": True,
            "firstName": "Example",
            "lastName": "Example",
            "emailVerified": True
        },
    ]
    for user in users:
        try:
            user_id = keycloak_admin.create_user(user, exist_ok=True)
            keycloak_admin.set_user_password(  # noqa
                user_id, password='test', temporary=False)  # noqa
        except KeycloakPostError:
            pass

    # Add groups to users
    groups_and_users = {
        'superusers': ['test_superuser_1'],
        'members': ['test_superuser_1', 'test_member_1', 'test_member_2']
    }
    for group_name, user_names in groups_and_users.items():
        group_id = keycloak_admin.get_group_by_path(f'/{group_name}')['id']
        for user_name in user_names:
            user_id = keycloak_admin.get_user_id(user_name)
            keycloak_admin.group_user_add(user_id, group_id)
