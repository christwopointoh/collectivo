"""Serializers of the profiles extension."""

from rest_framework import serializers

from collectivo.utils.serializers import UserIsPk

from . import models
from .schemas import (
    profile_register_schema,
    profile_schema,
    profile_user_schema,
)


class ProfileSettingsSerializer(serializers.ModelSerializer):
    """Serializer for profile settings."""

    class Meta:
        """Serializer settings."""

        label = "Profile Settings"
        model = models.ProfileSettings
        exclude = ["id"]


class ProfileBaseSerializer(UserIsPk):
    """Base serializer for member serializers with extra schema attributes."""


class ProfileAdminSerializer(ProfileBaseSerializer):
    """Serializer for admins to manage profiles."""

    class Meta:
        """Serializer settings."""

        label = "Profile"
        model = models.UserProfile
        fields = "__all__"
        read_only_fields = ["user"]
        schema = profile_schema


class ProfileHistorySerializer(ProfileBaseSerializer):
    """Serializer for admins to manage profile history."""

    class Meta:
        """Serializer settings."""

        label = "Profile"
        model = models.UserProfile.history.model
        fields = "__all__"


class ProfileRegisterSerializer(serializers.ModelSerializer):
    """Serializer to register profile including names."""

    user__first_name = serializers.CharField(
        source="user.first_name", required=False
    )
    user__last_name = serializers.CharField(
        source="user.last_name", required=False
    )

    class Meta:
        """Serializer settings."""

        label = "Profile"
        model = models.UserProfile
        exclude = ["user", "notes", "is_registered"]
        schema = profile_register_schema
        settings = models.ProfileSettings

    def update(self, instance, validated_data):
        """Update user fields seperately."""
        user_fields = validated_data.pop("user")
        obj = super().update(instance, validated_data)
        for key, value in user_fields.items():
            setattr(obj.user, key, value)
            obj.user.save()
        return obj


class ProfileUserSerializer(serializers.ModelSerializer):
    """Serializer for members to manage their own data."""

    class Meta:
        """Serializer settings."""

        label = "Profile"
        model = models.UserProfile
        exclude = ["user", "notes", "is_registered"]
        schema = profile_user_schema
        settings = models.ProfileSettings
