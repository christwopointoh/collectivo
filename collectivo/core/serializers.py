"""Serializers of the core extension."""
import logging

from django.contrib.auth import get_user_model
from django.db import models
from rest_framework import serializers

from collectivo.core.stores import main_store
from collectivo.tags.models import Tag

from .models import (
    CoreSettings,
    Endpoint,
    EndpointGroup,
    Permission,
    PermissionGroup,
)

User = get_user_model()
Group = User.groups.field.related_model
serializer_field_mapping = serializers.ModelSerializer.serializer_field_mapping
logger = logging.getLogger(__name__)


class CoreSettingsSerializer(serializers.ModelSerializer):
    """Serializer for core settings."""

    class Meta:
        """Serializer settings."""

        model = CoreSettings
        fields = "__all__"


class EndpointSerializer(serializers.ModelSerializer):
    """Serializer for endpoints."""

    class Meta:
        """Serializer settings."""

        model = Endpoint
        fields = "__all__"


class EndpointGroupSerializer(serializers.ModelSerializer):
    """Serializer for endpoint groups."""

    class Meta:
        """Serializer settings."""

        model = EndpointGroup
        fields = "__all__"


class PermissionSerializer(serializers.ModelSerializer):
    """Serializer for permissions."""

    class Meta:
        """Serializer settings."""

        model = Permission
        fields = "__all__"


class PermissionGroupSerializer(serializers.ModelSerializer):
    """Serializer for permission groups."""

    class Meta:
        """Serializer settings."""

        model = PermissionGroup
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    """Serializer for members to manage their own data."""

    # TODO: Get through groups
    # permissions = serializers.PrimaryKeyRelatedField(
    #     many=True, queryset=Permission.objects.all()
    # )
    permission_groups = serializers.PrimaryKeyRelatedField(
        many=True, queryset=PermissionGroup.objects.all()
    )

    class Meta:
        """Serializer settings."""

        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "permission_groups",
        ]
        read_only_fields = ["id"]


class UserProfilesSerializer(serializers.ModelSerializer):
    """Serializer of user, including the fields of all profiles."""

    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()

    # TODO: Load through TagProfile
    tags = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Tag.objects.all()
    )

    # Define serializer fields based on registered profiles in store
    # TODO: Get field settings from serializer
    # TODO: Make fields editable for bulk edit
    # TODO: Support foreign key and onetoone fields
    profile_serializers = main_store.user_profiles_admin_serializers
    for profile_serializer in profile_serializers:
        profile = profile_serializer.Meta.model
        _related_name = profile._meta.get_field("user")._related_name
        for field in profile._meta.get_fields():
            _field_class = serializer_field_mapping.get(field.__class__)
            if _field_class:
                if hasattr(field, "choices") and field.choices:
                    locals()[
                        f"{_related_name}__{field.attname}"
                    ] = serializers.ChoiceField(
                        source=f"{_related_name}.{field.attname}",
                        choices=field.choices,
                        read_only=True,
                    )
                else:
                    locals()[
                        f"{_related_name}__{field.attname}"
                    ] = _field_class(
                        source=f"{_related_name}.{field.attname}",
                        read_only=True,
                    )
            elif field.__class__ is models.OneToOneField:
                logger.warning(
                    "OneToOneField not supported in UserProfilesSerializer."
                )
            elif field.__class__ is models.ForeignKey:
                logger.warning(
                    "ForeignKey not supported in UserProfilesSerializer."
                )
            elif field.__class__ is models.ManyToManyField:
                locals()[
                    f"{_related_name}__{field.attname}"
                ] = serializers.PrimaryKeyRelatedField(
                    source=f"{_related_name}.{field.attname}",
                    read_only=True,
                    many=True,
                )

    class Meta:
        """Serializer settings."""

        model = User
        exclude = [
            "username",
            "password",
            "is_superuser",
            "is_staff",
            "is_active",
            "user_permissions",
            "last_login",
            "date_joined",
        ]
        read_only_fields = ["user"]


class GroupSerializer(serializers.ModelSerializer):
    """Serializer for members to manage their own data."""

    class Meta:
        """Serializer settings."""

        model = Group
        fields = ["name"]
