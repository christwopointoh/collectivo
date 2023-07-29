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


class EmailAutomation(models.Model):
    """An automation that sends emails to users."""

    class Meta:
        """Model settings."""

        unique_together = ("name", "extension")

    objects = NameManager()
    history = HistoricalRecords()

    name = models.CharField(max_length=255)
    label = models.CharField(max_length=255)
    is_active = models.BooleanField(
        default=False,
        verbose_name="Active",
        help_text=(
            "If checked, this automation will be active and send emails."
        ),
    )
    description = models.TextField()
    extension = models.ForeignKey(
        "extensions.Extension",
        on_delete=models.CASCADE,
    )
    admin_only = models.BooleanField(default=False)

    template = models.ForeignKey(
        "emails.EmailTemplate",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="automations",
    )
    
    admin_template = models.ForeignKey(
        "emails.EmailTemplate",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="automations_admin",
    )
    
    admin_recipients = models.ManyToManyField(
        get_user_model(),
        verbose_name="Recipients",
        related_name="admin_email_automations",
        blank=True,
    )

    def send(self, recipients, context=None):
        """Send emails to recipients."""
        if self.is_active:
            # Generate email campaign for admins from automation
            admin_campaign = EmailCampaign.objects.create(
                template=self.admin_template,
                recipients=self.admin_recipients.all(),
                extension=self.extension,
            )
            admin_campaign.save()
            admin_campaign.send(context=context)
            
            if not self.automation.admin_only:
                # Generate email campaign for end users from automation
                user_campaign = EmailCampaign.objects.create(
                    template=self.template,
                    recipients=recipients,
                    extension=self.extension,
                )
                user_campaign.save()
                user_campaign.send(context=context)


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
        "emails.EmailDesign", on_delete=models.PROTECT, null=True
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

    def send(self, context=None):
        """Send emails to recipients."""
        self.sent = timezone.now()
        self.status = "pending"
        self.save()

        # Generate emails from template
        email_batches = self.create_email_batches(context=context)

        # Create a chain of async tasks to send emails
        results = {"n_sent": 0, "campaign": self}
        tasks = []
        tasks.append(send_mails_async.s(results, email_batches.pop(0)))
        for email_batch in email_batches:
            tasks.append(send_mails_async.s(email_batch))
        tasks.append(send_mails_async_end.s())
        try:
            chain(*tasks)()
        except Exception as e:
            self.status = "failure"
            self.status_message = str(e)
            self.save()
            raise e

    def create_email_batches(self, context=None):
        """Create a list of emails, split into batches."""
        if self.template.design is not None:
            body_with_design_applied = self.template.design.body.replace("{{content}}", self.template.body)
        else:
            body_with_design_applied = self.template.body
            
        from_email = settings.DEFAULT_FROM_EMAIL
        emails = []
        for recipient in self.recipients.all():
            body_html = Template(body_with_design_applied).render(
                Context({"user": recipient, **(context or {})})
            )
            body_text = html2text(body_html)
            if recipient.email in (None, ""):
                self.status = "failure"
                self.status_message = f"{recipient} has no email."
                self.save()
                raise ValueError(self.status_message)
            email = EmailMultiAlternatives(
                self.template.subject, body_text, from_email, [recipient.email]
            )
            email.attach_alternative(body_html, "text/html")
            emails.append(email)

        # Split recipients into batches
        n = 20  # TODO Get this number from the settings
        return [emails[i : i + n] for i in range(0, len(emails), n)]
