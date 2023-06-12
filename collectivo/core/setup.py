"""Setup function of the core extension."""

from django.conf import settings
from django.contrib.auth import get_user_model

from collectivo.core.apps import CoreConfig
from collectivo.core.models import Permission, PermissionGroup
from collectivo.extensions.models import Extension
from collectivo.menus.models import Menu, MenuItem
from collectivo.utils.dev import DEV_USERS

User = get_user_model()


def setup():
    """Initialize extension after database is ready."""

    extension = Extension.register(
        name=CoreConfig.name, description=CoreConfig.description, built_in=True
    )

    superuser = PermissionGroup.objects.get_or_create(
        name="superuser", extension=extension
    )[0]
    coreadmin = Permission.objects.register(name="admin", extension=extension)
    superuser.permissions.add(coreadmin)

    # User menu
    Menu.register(name="main", extension=extension)
    MenuItem.register(
        name="profile",
        label="Profile",
        extension=extension,
        route=extension.name + "/profile",
        icon_name="pi-user",
        parent="main",
    )
    MenuItem.register(
        name="logout",
        label="Log out",
        extension=extension,
        route=extension.name + "/logout",
        icon_name="pi-sign-out",
        parent="main",
        order=99,
    )

    # Create admin menu
    Menu.register(name="admin", extension=extension)
    MenuItem.register(
        name="users",
        label="Users",
        extension=extension,
        parent="admin",
        route=extension.name + "/users",
        icon_name="pi-users",
        requires_perm=("admin", "core"),
        order=00,
    )
    MenuItem.register(
        name="settings",
        label="Settings",
        extension=extension,
        parent="admin",
        route=extension.name + "/settings",
        icon_name="pi-cog",
        requires_perm=("admin", "core"),
        order=100,
    )

    if settings.COLLECTIVO["example_data"] is True:
        for first_name in DEV_USERS:
            email = f"test_{first_name}@example.com"
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                user = User.objects.create(email=email)
            user.username = email
            user.first_name = first_name[0].upper() + first_name[1:]
            user.last_name = "Example"
            user.save()

            # Give user permissions
            if first_name == "superuser":
                user.permission_groups.add(superuser)
