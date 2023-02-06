"""Serializers of the extension."""
from rest_framework import serializers
from .models import TapirModel


class TapirSerializer(serializers.ModelSerializer):
    """Serializer for Tapir model."""

    class Meta:
        """Serializer settings."""

        model = TapirModel
        fields = '__all__'
