"""Models of the memberships_emails extension."""
from django.db import models
from django.db.models import signals

from collectivo.memberships.models import MembershipType


class MembershipEmails(models.Model):
    """Mediator between a membership type and email templates."""

    membership_type = models.OneToOneField(
        "memberships.MembershipType",
        on_delete=models.CASCADE,
        primary_key=True,
        related_name="emails",
    )
    template_started = models.ForeignKey(
        "emails.EmailTemplate",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="membership_started",
    )
    template_accepted = models.ForeignKey(
        "emails.EmailTemplate",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="membership_accepted",
    )
    template_ended = models.ForeignKey(
        "emails.EmailTemplate",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="membership_ended",
    )


def create_memberships_emails_connector(sender, instance, created, **kwargs):
    """Create connector when membership type is created."""
    if created:
        MembershipEmails.objects.create(membership_type=instance)


signals.post_save.connect(
    create_memberships_emails_connector,
    sender=MembershipType,
    dispatch_uid="create_memberships_emails_connector",
    weak=False,
)
