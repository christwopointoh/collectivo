"""Serializers of the profiles extension."""

from rest_framework import serializers

from collectivo.utils.serializers import UserIsPk

from . import models

conditions = {
    "natural": {
        "field": "person_type",
        "condition": "exact",
        "value": "natural",
    },
    "legal": {"field": "person_type", "condition": "exact", "value": "legal"},
}

schema_attrs = {
    "birthday": {"visible": conditions["natural"], "required": True},
    "occupation": {"visible": conditions["natural"], "required": True},
    "legal_name": {"visible": conditions["legal"], "required": True},
    "legal_type": {"visible": conditions["legal"], "required": True},
    "legal_id": {"visible": conditions["legal"], "required": True},
}


class ProfileBaseSerializer(UserIsPk):
    """Base serializer for member serializers with extra schema attributes."""


class ProfileAdminSerializer(ProfileBaseSerializer):
    """Serializer for admins to manage members."""

    # Display user as id so that the frontend always gets an id field
    id = serializers.SerializerMethodField()

    class Meta:
        """Serializer settings."""

        label = "Profile"
        model = models.UserProfile
        fields = "__all__"
        read_only_fields = ["user"]
        schema_attrs = schema_attrs


class ProfileUserSerializer(ProfileBaseSerializer):
    """Serializer for members to manage their own data."""

    class Meta:
        """Serializer settings."""

        label = "Profile"
        model = models.UserProfile
        exclude = ["user", "notes"]
        schema_attrs = schema_attrs
