"""Serializers of the dashboard extension."""
from rest_framework import serializers
from .models import DashboardTile


class DashboardTileSerializer(serializers.ModelSerializer):
    """Serializer for dashboard tiles."""

    class Meta:
        """Serializer settings."""

        model = DashboardTile
        fields = '__all__'
