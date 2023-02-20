"""Models of the emails module."""
from django.db import models


class EmailDesign(models.Model):
    """A design of an email."""

    name = models.CharField(max_length=255, unique="True")
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return a string representation of the object."""
        return self.name


class EmailTemplate(models.Model):
    """A template of an email."""

    name = models.CharField(max_length=255, unique="True")
    design = models.ForeignKey(
        "emails.EmailDesign", on_delete=models.SET_NULL, null=True
    )
    subject = models.CharField(max_length=255)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    tag = models.ForeignKey(
        "members.MemberTag",
        on_delete=models.SET_NULL,
        null=True,
        help_text="This tag will be added to recipients if campaign is sent.",
    )

    def __str__(self):
        """Return a string representation of the object."""
        return self.name


class EmailCampaign(models.Model):
    """A mass email that is being processed or has been sent."""

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
    created = models.DateTimeField(auto_now_add=True)
    sent = models.DateTimeField(null=True)
    recipients = models.ManyToManyField("members.Member")
    automation = models.ForeignKey(
        "emails.EmailAutomation",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    def __str__(self):
        """Return a string representation of the object."""
        return (
            "Email campaign "
            f"({self.id}, {self.status}, {self.template.name})"
        )


class EmailAutomation(models.Model):
    """A rule to automatically send emails to members."""

    template = models.ForeignKey(
        "emails.EmailTemplate", on_delete=models.SET_NULL, null=True
    )
    created = models.DateTimeField(auto_now_add=True)
    trigger = models.CharField(
        max_length=10,
        choices=[
            ("new_member", "new_member"),
        ],
    )

    def __str__(self):
        """Return a string representation of the object."""
        return f"{self.trigger} ({self.id})"


class EmailSettings(models.Model):
    """Settings for the emails module."""

    email_host = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        default="localhost",
        label="Email host",
        help_text="Address of an SMTP server that is used for sending emails.",
    )
    email_host_user = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        label="Email user",
        help_text="Username to use for the SMTP server.",
    )
    email_host_password = models.CharField(
        max_length=255,
        write_only=True,
        blank=True,
        null=True,
        label="Email password",
        help_text="Password to use for the SMTP server.",
    )
    email_connection = models.CharField(
        default="None",
        choices=[
            "TLS",
            "SSL",
            "None",
        ],
        label="Email connection",
        help_text="The type of connection to use for the SMTP server.",
    )
    email_port = models.IntegerField(
        default=465,
        blank=True,
        null=True,
        label="Email port",
        help_text="The port to use for the SMTP server.",
    )
    email_from = models.EmailField(
        max_length=255,
        blank=True,
        null=True,
        label="Sender email",
        help_text="The email address to use for sending emails.",
    )
    email_to = models.EmailField(
        max_length=255,
        blank=True,
        null=True,
        label="Admin email",
        help_text="The email address to use to send admin notifications to.",
    )
    email_sending_rate = models.IntegerField(
        default=100,
        blank=True,
        null=True,
        label="Email sending rate",
        help_text="The maximum number of emails to send per minute.",
    )

    def __str__(self):
        """Return a string representation of the object."""
        return "Email settings"
