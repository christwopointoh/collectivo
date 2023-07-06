"""Setup function of the payments extension."""
from django.contrib.auth import get_user_model

from collectivo.core.models import Permission, PermissionGroup
from collectivo.extensions.models import Extension
from collectivo.menus.models import MenuItem

from .apps import PaymentsConfig
from .models import Account, PaymentProfile

User = get_user_model()


def setup(sender, **kwargs):
    """Initialize extension after database is ready."""

    extension = Extension.objects.register(
        name=PaymentsConfig.name,
        description=PaymentsConfig.description,
        built_in=True,
    )

    perm_names = [
        "view_payments",
        "edit_payments",
    ]
    superuser = PermissionGroup.objects.get(name="superuser")
    for perm_name in perm_names:
        perm = Permission.objects.register(
            name=perm_name,
            label=perm_name.replace("_", " ").capitalize(),
            description=f"Can {perm_name.replace('_', ' ')}",
            extension=extension,
        )
        superuser.permissions.add(perm)

    MenuItem.objects.register(
        name="payments_admin",
        label="Payments",
        extension=extension,
        route=extension.name + "/admin",
        icon_name="pi-money-bill",
        requires_perm=("view_payments", "payments"),
        parent="admin",
        order=20,
    )

    # Create payment profiles and accounts
    users = User.objects.filter(payment_profile__isnull=True)
    for user in users:
        PaymentProfile.objects.get_or_create(user=user)
    users = User.objects.filter(account__isnull=True)
    for user in users:
        Account.objects.get_or_create(user=user)
