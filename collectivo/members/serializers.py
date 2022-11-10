"""Serializers of the members extension."""
from rest_framework import serializers
from .models import Member


admin_attrs = ('user_id', 'admin_attr', )  # Write access only for admins
create_attrs = ('create_attr', )  # Write access only for post or admins


class MemberCreateSerializer(serializers.ModelSerializer):
    """Serializer for members to create themselves."""

    class Meta:
        """Serializer settings."""

        model = Member
        fields = '__all__'
        read_only_fields = admin_attrs


class MemberSerializer(serializers.ModelSerializer):
    """Serializer for members to manage their own data."""

    class Meta:
        """Serializer settings."""

        model = Member
        fields = '__all__'
        read_only_fields = admin_attrs + create_attrs


class MemberAdminSerializer(serializers.ModelSerializer):
    """Serializer for admins to manage members."""

    class Meta:
        """Serializer settings."""

        model = Member
        fields = '__all__'
