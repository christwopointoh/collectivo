"""Populate collectivo & keycloak with test users."""
import logging
from collectivo.utils import get_auth_manager, get_user_model
from keycloak.exceptions import KeycloakPostError


logger = logging.getLogger(__name__)

N_TEST_MEMBERS = 15


def populate_keycloak_with_test_data():
    """Add users, groups, and roles to keycloak."""
    logger.debug('Creating test-population')
    auth_manager = get_auth_manager()

    # Add users
    superusers = [
        {
            "email": "test_superuser@example.com",
            "username": "test_superuser@example.com",
            "enabled": True,
            "firstName": "Example",
            "lastName": "Example",
            "emailVerified": True,
        },
    ]

    members = [
        {
            "email": f"test_member_{str(i).zfill(2)}@example.com",
            "username": f"test_member_{str(i).zfill(2)}@example.com",
            "enabled": True,
            "firstName": f"Test Member {str(i).zfill(2)}",
            "lastName": "Example",
            "emailVerified": True
        }
        for i in range(1, N_TEST_MEMBERS)
    ] + superusers

    users = [
        {
            "email": "test_user_not_verified@example.com",
            "username": "test_user_not_verified@example.com",
            "enabled": True,
            "firstName": "Example",
            "lastName": "Example",
            "emailVerified": False
        },
        {
            "email": "test_user_not_member@example.com",
            "username": "test_user_not_member@example.com",
            "enabled": True,
            "firstName": "Example",
            "lastName": "Example",
            "emailVerified": True
        },
    ] + members

    for user in users:
        try:
            user_id = auth_manager.create_user(user, exist_ok=True)
            auth_manager.set_user_password(  # noqa
                user_id, password='test', temporary=False)  # noqa
        except KeycloakPostError:
            pass

    # Add groups to users
    groups_and_users = {
        'superusers': [d['email'] for d in superusers],
    }
    for group_name, user_names in groups_and_users.items():
        for user_name in user_names:
            user_id = auth_manager.get_user_id(user_name)
            auth_manager.add_user_to_group(user_id, group_name)

    # Make members into members
    # This automatically adds them to the group 'members'
    for member in members:
        user_id = auth_manager.get_user_id(member['username'])
        payload = {
            'user_id': user_id,

            'email': member['email'],
            'email_verified': member['emailVerified'],

            'first_name': member['firstName'],
            'last_name': member['lastName'],
        }
        get_user_model().objects.get_or_create(**payload)
