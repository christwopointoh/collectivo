"""Serializers of the memberships extension."""
from django.contrib.auth import get_user_model
from rest_framework import serializers

from collectivo.utils.serializers import UserFields

from . import models
from .statistics import calculate_statistics

try:
    from collectivo.emails.models import EmailTemplate

    emails_installed = True
except ImportError:
    emails_installed = False

User = get_user_model()


class MembershipSerializer(UserFields):
    """Serializer for memberships."""

    try:
        import collectivo.tags

        user__tags = serializers.PrimaryKeyRelatedField(
            many=True,
            source="user.tags",
            read_only=True,
            label="Tags",
        )
    except ImportError:
        pass
    try:
        import collectivo.profiles

        user__profile__person_type = serializers.CharField(
            source="user.profile.person_type",
            read_only=True,
            label="Person type",
        )
    except ImportError:
        pass

    class Meta:
        """Serializer settings."""

        model = models.Membership
        fields = "__all__"
        read_only_fields = ["id", "number"]


class MembershipSelfSerializer(serializers.ModelSerializer):
    """Serializer for memberships."""

    class Meta:
        """Serializer settings."""

        model = models.Membership
        fields = "__all__"
        depth = 1

    def get_fields(self):
        """Set all fields to read only except shares_signed."""
        fields = super().get_fields()
        for field_name, field in fields.items():
            if field_name != "shares_signed":
                field.read_only = True
        return fields

    def validate(self, data):
        """Validate the data."""
        if data.get("shares_signed", None) is not None:
            if data["shares_signed"] < self.instance.shares_signed:
                raise serializers.ValidationError(
                    "You cannot lower the number of shares you signed."
                )
            if self.instance.type.shares_number_custom_min is not None:
                if (
                    data["shares_signed"]
                    < self.instance.type.shares_number_custom_min
                ):
                    raise serializers.ValidationError(
                        "The number of shares you signed is too low."
                    )
            if self.instance.type.shares_number_custom_max is not None:
                if (
                    data["shares_signed"]
                    > self.instance.type.shares_number_custom_max
                ):
                    raise serializers.ValidationError(
                        "The number of shares you signed is too high."
                    )

        return data


class MembershipProfileSerializer(serializers.ModelSerializer):
    """Serializer for tag profiles."""

    memberships = serializers.PrimaryKeyRelatedField(
        many=True, queryset=models.Membership.objects.all()
    )

    class Meta:
        """Serializer settings."""

        label = "Memberships"
        model = User
        fields = ["id", "memberships"]
        read_only_fields = ["id", "memberships"]


email_fields = [
    "emails__template_started",
    "emails__template_accepted",
    "emails__template_ended",
]


class MembershipTypeSerializer(serializers.ModelSerializer):
    """Serializer for membership types."""

    statistics = serializers.SerializerMethodField()

    if emails_installed:
        emails__template_started = serializers.PrimaryKeyRelatedField(
            source="emails.template_started",
            queryset=EmailTemplate.objects.all(),
            required=False,
            allow_null=True,
            help_text=(
                "The email template to send when a membership of this type is"
                " started (i.e. when the field date_started is set)."
            ),
        )
        emails__template_accepted = serializers.PrimaryKeyRelatedField(
            source="emails.template_accepted",
            queryset=EmailTemplate.objects.all(),
            required=False,
            allow_null=True,
            help_text=(
                "The email template to send when a membership of this type is"
                " accepted (i.e. when the field date_accepted is set)."
            ),
        )
        emails__template_ended = serializers.PrimaryKeyRelatedField(
            source="emails.template_ended",
            queryset=EmailTemplate.objects.all(),
            required=False,
            allow_null=True,
            help_text=(
                "The email template to send when a membership of this type is"
                " ended (i.e. when the field date_ended is set)."
            ),
        )

    class Meta:
        """Serializer settings."""

        model = models.MembershipType
        fields = "__all__"
        read_only_fields = ["id"]

    def get_statistics(self, obj):
        """Get statistics for this membership type."""
        return calculate_statistics(obj)

    def create(self, validated_data):
        """Create a new membership."""
        if not emails_installed:
            return super().create(validated_data)
        email_data = {}
        for field in email_fields:
            if field in validated_data:
                email_data[field] = validated_data.pop(field)
        obj = super().create(validated_data)
        for field, data in email_data.items():
            setattr(obj.emails, field, data)
        obj.emails.save()
        return obj

    def update(self, instance, validated_data):
        """Update an existing membership."""
        if not emails_installed:
            return super().update(validated_data)
        email_data = {}
        for field in email_fields:
            if field in validated_data:
                email_data[field] = validated_data.pop(field)
        obj = super().update(validated_data)
        for field, data in email_data.items():
            setattr(obj.emails, field, data)
        obj.emails.save()
        return obj


class MembershipStatusSerializer(serializers.ModelSerializer):
    """Serializer for membership statuses."""

    class Meta:
        """Serializer settings."""

        model = models.MembershipStatus
        fields = "__all__"
        read_only_fields = ["id"]
