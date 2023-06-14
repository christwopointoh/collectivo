"""Signals of the memberships extension."""
from django.contrib.auth import get_user_model
from django.db.models import signals

from collectivo.extensions.models import Extension

from .models import Membership, MembershipType

try:
    from collectivo.payments.models import Invoice, ItemTypeCategory

    def update_shares_paid(sender, instance, created, **kwargs):
        """Update shares_paid of a membership after an invoice is saved."""

        extension = Extension.objects.get(name="memberships")
        item_category = ItemTypeCategory.objects.get_or_create(
            name="Shares", extension=extension
        )[0]
        entries = instance.items.filter(
            type__category=item_category,
            invoice__status="paid",
        )
        if not entries.exists():
            return

        for entry in entries:
            membership_type = MembershipType.objects.get(name=entry.type.name)
            shares_paid = (
                sum([entry.amount * entry.price for entry in entries])
                / membership_type.shares_amount_per_share
            )
            membership = Membership.objects.get(
                user=instance.payment_from.user,
                type=membership_type,
            )
            membership.shares_paid = shares_paid
            membership.save()

    signals.post_save.connect(
        update_shares_paid,
        sender=Invoice,
        dispatch_uid="update_shares_paid",
        weak=False,
    )

except ImportError:
    pass
