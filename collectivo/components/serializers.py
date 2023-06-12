"""Serializers of the components module."""
from rest_framework import serializers

from .models import Component


class ComponentSerializer(serializers.ModelSerializer):
    """Serializer for component objects."""

    class Meta:
        """Serializer settings."""

        model = Component
        fields = "__all__"
        depth = 1
