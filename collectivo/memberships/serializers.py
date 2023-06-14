"""Serializers of the memberships extension."""
from django.contrib.auth import get_user_model
from django.db.models import Avg, Max, Sum
from rest_framework import serializers

from collectivo.utils.serializers import UserFields

from . import models
from .statistics import calculate_statistics

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


class MembershipTypeSerializer(serializers.ModelSerializer):
    """Serializer for membership types."""

    statistics = serializers.SerializerMethodField()

    class Meta:
        """Serializer settings."""

        model = models.MembershipType
        fields = "__all__"
        read_only_fields = ["id"]

    def get_statistics(self, obj):
        """Get statistics for this membership type."""
        return calculate_statistics(obj)


class MembershipStatusSerializer(serializers.ModelSerializer):
    """Serializer for membership statuses."""

    class Meta:
        """Serializer settings."""

        model = models.MembershipStatus
        fields = "__all__"
        read_only_fields = ["id"]
