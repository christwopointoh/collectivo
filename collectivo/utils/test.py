"""Tests for the collectivo utility functions."""
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from collectivo.core.models import Permission, PermissionGroup

User = get_user_model()


def create_testuser(
    username="testuser",
    perms: list[str] = None,
    extension=None,
    superuser: bool = False,
) -> tuple[APIClient, User]:
    """Return a user with given permissions."""
    try:
        User.objects.get(username=username).delete()
    except User.DoesNotExist:
        pass
    user = User.objects.create_user(username=username)
    if superuser:
        user.permission_groups.add(
            PermissionGroup.objects.get_or_create(
                name="superuser", extension__name="core"
            )[0]
        )
    group = PermissionGroup.objects.get_or_create(
        name=f"test_group_{user.id}"
    )[0]

    user.permission_groups.add(group)
    perms = perms or []
    for perm in perms:
        group.permissions.add(
            Permission.objects.get_or_create(name=perm, extension=extension)[0]
        )
    group.save()
    user.save()

    return user


def create_testadmin(
    username="testadmin",
    perms: list[tuple] = None,
    extension=None,
    superuser: bool = True,
) -> tuple[APIClient, User]:
    """Return a superuser with given permissions."""
    return create_testuser(username, perms, extension, superuser)
