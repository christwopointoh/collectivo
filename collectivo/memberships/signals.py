"""Signals of the memberships extension."""
from django.db.models import signals

try:
    from collectivo.payments.models import Invoice

    def update_shares_paid(sender, instance: Invoice, created, **kwargs):
        """Update shares_paid of a membership after an invoice is saved."""

        memberships = instance.payment_from.user.memberships.all()
        for membership in memberships:
            membership.update_shares_paid()

    signals.post_save.connect(
        update_shares_paid,
        sender=Invoice,
        dispatch_uid="update_shares_paid",
        weak=False,
    )

except ImportError:
    pass
