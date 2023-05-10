"""Setup function of the core extension."""

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.urls import reverse

from collectivo.core.apps import CoreConfig
from collectivo.core.models import Endpoint, EndpointGroup
from collectivo.extensions.models import Extension
from collectivo.menus.models import Menu, MenuItem
from collectivo.utils.dev import DEV_USERS

User = get_user_model()


def setup():
    """Initialize extension after database is ready."""

    extension = Extension.register(
        name=CoreConfig.name, description=CoreConfig.description, built_in=True
    )

    superuser = Group.objects.get_or_create(
        name="collectivo.core.admin",
    )[0]

    # Create core endpoint groups
    endpoint_groups = {
        "remote_entries": None,
        "admin_settings": None,
        "user_settings": None,
        "admin_profiles": None,
        "user_profiles": None,
    }
    for name in endpoint_groups:
        endpoint_groups[name] = EndpointGroup.objects.register(
            name=name, extension=extension
        )

    # Add core settings to admin settings group
    endpoint = Endpoint.objects.register(
        name="core_settings",
        path=reverse("collectivo.core:settings"),
        extension=extension,
    )
    endpoint_groups["admin_settings"].endpoints.add(endpoint)
    endpoint_groups["admin_settings"].save()

    # User menu
    Menu.register(name="main", extension=extension)
    MenuItem.register(
        name="profile",
        label="Profile",
        extension=extension,
        component="profile",
        icon_name="pi-user",
        parent="main",
    )
    MenuItem.register(
        name="logout",
        label="Log out",
        extension=extension,
        component="logout",
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
        component="users",
        icon_name="pi-users",
        requires_group="collectivo.core.admin",
        order=00,
    )
    MenuItem.register(
        name="settings",
        label="Settings",
        extension=extension,
        parent="admin",
        component="settings",
        icon_name="pi-cog",
        requires_group="collectivo.core.admin",
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
                user.groups.add(superuser)
