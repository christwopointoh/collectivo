# collectivo

A modular framework to build participative community platforms.

## Overview

The collectivo framework consists of a backend (this repository)
and a frontend ([collectivo-ux](https://github.com/MILA-Wien/collectivo-ux/)) application.
Different community tools can be added to collectivo through extensions.

## Development

The following development environment is used in our team:

1. [Docker](https://www.docker.com/), Version >= 20.10
2. [VisualStudioCode](https://code.visualstudio.com/) (VSCode)

To run and test the app with docker:

1. Build a development server and run: `docker compose build`
2. Add the following line to your `/etc/hosts/` file: `127.0.0.1 keycloak collectivo.local`
3. To start a development server, run: `docker compose up -d`
    - Optional: To also set up a development server for the frontend, follow the instructions at [collectivo-ux](https://github.com/MILA-Wien/collectivo-ux/).
4. The API will then be available at `collectivo.local:8000/api/docs/`.
5. The frontend will be available at `collectivo.local:8001` (or `collectivo.local:5137` if you set up a development server via [collectivo-ux](https://github.com/MILA-Wien/collectivo-ux/)).
6. To perform tests and linting, run: `docker compose run --rm collectivo sh -c "python manage.py test && flake8"`

### The collectivo-test-app

The default docker instructions will install collectivo within the collectivo-test-app. This test app initializes with the following test users:

- `test_superuser@example.com`
- `test_member_01@example.com`, `test_member_02@example.com`, ..., `test_member_15@example.com`
- `test_user_not_verified@example.com`
- `test_user_not_member@example.com`

The password for all users is `test`.

## Documentation

### Auth extension

The auth extension manages user authentication and authorization.
To activate the extension, add the following line in `settings.py`:

```python
INSTALLED_APPS = [
    ...
    'collectivo.auth'
]
```

Currently, the only supported authentication server is [keycloak](https://www.keycloak.org/).
To activate authentication via, add the following line in `settings.py`:

```python
MIDDLEWARE = [
    ...
    'collectivo.auth.middleware.KeycloakMiddleware'
]
```

The following attributes can be used to configure the auth extension in the collectivo settings within `settings.py`:

```python
COLLECTIVO = {
    ...
    # Configuration for auth.middleware.KeycloakMiddleware
    'auth_keycloak_config': {
        'SERVER_URL': 'http://keycloak:8080',
        'REALM_NAME': 'collectivo',
        'CLIENT_ID': 'collectivo',
        'CLIENT_SECRET_KEY': '**********'
    },
    # Define user groups and their respective roles
    # These will be automatically added to keycloak.
    # Check other extensions to see possible roles.
    'auth_groups_and_roles': {
        'members': ['members_user', ...],
        'superuser': ['collectivo_admin', 'members_admin', ...]
    },
}
```

Further information:
- To export the keycloak realm including users run `docker compose exec -u 0 keycloak /opt/keycloak/bin/kc.sh export --dir /tmp/export --realm collectivo --users realm_file` Note: exporting the realm via the gui doesn't include the users. The exported files is then in the `./docker/keycloak/export` folder.

### Members extension

The members extension can be used to manage member data.

- Roles:
    - `members_user`
    - `members_admin`
- Groups:
    - `members`: If this group exists, members will automatically be added to this group.
- API:
    - `/members/v1/me`
        - `POST`: Users that are not yet members can sign up as members.
        - All other views: Members can manage their own data (required role: `members_user`).
    - `/members/v1/members`:
        - All views: Manage the data of all users (required role: `members_admin`).
