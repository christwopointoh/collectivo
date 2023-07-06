"""Setup function of the payments extension."""
from django.contrib.auth import get_user_model

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

    MenuItem.objects.register(
        name="payments_admin",
        label="Payments",
        extension=extension,
        route=extension.name + "/admin",
        icon_name="pi-money-bill",
        requires_perm=("admin", "core"),
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
