"""Setup function of the payments extension."""
from collectivo.core.stores import main_store
from collectivo.extensions.models import Extension
from collectivo.menus.models import MenuItem

from . import serializers
from .apps import PaymentsConfig


def setup(sender, **kwargs):
    """Initialize extension after database is ready."""

    extension = Extension.register(
        name=PaymentsConfig.name,
        description=PaymentsConfig.description,
        built_in=True,
    )

    main_store.user_profiles_admin_serializers.append(
        serializers.PaymentProfileSerializer
    )

    MenuItem.register(
        name="payments_admin",
        label="Payments",
        extension=extension,
        component="admin",
        icon_name="pi-money-bill",
        requires_perm=("admin", "core"),
        parent="admin",
        order=20,
    )
