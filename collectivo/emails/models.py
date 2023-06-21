"""Models of the emails module."""
from celery import chain
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives
from django.db import models
from django.template import Context, Template
from django.utils import timezone
from html2text import html2text
from simple_history.models import HistoricalRecords

from collectivo.utils.managers import NameManager

from .tasks import send_mails_async, send_mails_async_end


class EmailDesign(models.Model):
    """A design of an email, which can be applied to a template."""

    objects = NameManager()
    history = HistoricalRecords()

    name = models.CharField(max_length=255, unique="True")
    body = models.TextField()

    def __str__(self):
        """Return a string representation of the object."""
        return self.name


class EmailTemplate(models.Model):
    """A template of an email, which can be applied to a campaign."""

    objects = NameManager()
    history = HistoricalRecords()

    name = models.CharField(max_length=255, unique="True")
    design = models.ForeignKey(
        "emails.EmailDesign", on_delete=models.SET_NULL, null=True
    )
    subject = models.CharField(max_length=255)
    body = models.TextField()

    def __str__(self):
        """Return a string representation of the object."""
        return self.name


class EmailCampaign(models.Model):
    """An email campaign that can be used to send mass emails."""

    history = HistoricalRecords()

    template = models.ForeignKey(
        "emails.EmailTemplate", on_delete=models.SET_NULL, null=True
    )
    status = models.CharField(
        max_length=10,
        default="draft",
        choices=[
            ("draft", "draft"),
            ("pending", "pending"),
            ("success", "success"),
            ("failure", "failure"),
        ],
    )
    status_message = models.CharField(max_length=255, null=True)
    sent = models.DateTimeField(null=True)
    recipients = models.ManyToManyField(
        get_user_model(), related_name="emails"
    )
    extension = models.ForeignKey(
        "extensions.Extension",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="The extension that created this campaign.",
    )

    def __str__(self):
        """Return a string representation of the object."""
        return f"{self.template.name} ({self.sent})"

    def send(self):
        """Send emails to recipients."""
        campaign = self
        campaign.sent = timezone.now()
        campaign.status = "pending"
        campaign.save()

        # Prepare the emails
        template = campaign.template
        recipients = self.recipients.all()
        subject = template.subject
        body = template.body
        if template.design is not None:
            body = template.design.body.replace("{{content}}", template.body)
        from_email = settings.DEFAULT_FROM_EMAIL
        emails = []
        for recipient in recipients:
            body_html = Template(body).render(Context({"user": recipient}))
            body_text = html2text(body_html)
            if recipient.email in (None, ""):
                campaign.status = "failure"
                campaign.status_message = f"{recipient} has no email."
                campaign.save()
                raise ValueError(campaign.status_message)
            email = EmailMultiAlternatives(
                subject, body_text, from_email, [recipient.email]
            )
            email.attach_alternative(body_html, "text/html")
            emails.append(email)

        # Split recipients into batches
        n = 20  # TODO Get this number from the settings
        batches = [emails[i : i + n] for i in range(0, len(emails), n)]

        # Create a chain of async tasks to send the emails
        results = {"n_sent": 0, "campaign": campaign}
        tasks = []
        tasks.append(send_mails_async.s(results, batches.pop(0)))
        for batch in batches:
            tasks.append(send_mails_async.s(batch))
        tasks.append(send_mails_async_end.s())
        try:
            chain(*tasks)()
        except Exception as e:
            campaign.status = "failure"
            campaign.status_message = str(e)
            campaign.save()
            raise e
