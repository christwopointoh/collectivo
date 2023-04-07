"""Models of the dashboard extension."""
from django.contrib.auth.models import Group
from django.db import models

from collectivo.extensions.models import Extension
from collectivo.utils import get_instance
from collectivo.utils.models import RegisterMixin


class DashboardTile(models.Model, RegisterMixin):
    """A component that can be included in the dashboard."""

    class Meta:
        """Meta settings."""

        unique_together = ("name", "extension")

    name = models.CharField(max_length=255, unique=True)
    label = models.CharField(max_length=255, null=True, blank=True)
    extension = models.ForeignKey(
        "extensions.Extension",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    order = models.FloatField(default=1)
    requires_group = models.ForeignKey(
        "auth.Group",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        help_text="If set, the object will only be displayed to users with "
        "this group.",
    )

    source = models.CharField(
        max_length=255,
        choices=[
            ("db", "Content is defined in the content field of this model."),
            ("component", "Content is defined in a webcomponent."),
        ],
    )
    component = models.CharField(max_length=255)
    content = models.TextField(
        null=True,
        blank=True,
        help_text="HTML content to display inside the tile.",
    )
    # TODO Enable or remove
    # show_button = models.BooleanField(default=False)
    # button_label = models.CharField(max_length=255, null=True, blank=True)
    # button_link = models.CharField(max_length=255, null=True, blank=True)
    # button_type = models.CharField(
    #     max_length=255,
    #     choices=[
    #         ("internal", "Internal link"),
    #         ("external", "External link"),
    #     ],
    # )

    def __str__(self):
        """Return string representation of the model."""
        return self.name

    @classmethod
    def register(
        cls,
        name: str,
        extension: str | Extension,
        requires_group: str = None,
        **payload,
    ):
        """Register a new dashboard tile."""
        payload["extension"] = get_instance(Extension, extension)
        payload["requires_group"] = get_instance(Group, requires_group)
        return super().register(name=name, **payload)
