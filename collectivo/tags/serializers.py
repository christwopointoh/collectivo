"""Serializers of the tags extension."""
from django.contrib.auth import get_user_model
from rest_framework import serializers

from collectivo.utils.serializers import create_history_serializer

from . import models

User = get_user_model()


class TagSerializer(serializers.ModelSerializer):
    """Serializer for tags."""

    class Meta:
        """Serializer settings."""

        model = models.Tag
        fields = "__all__"
        read_only_fields = ("id", "extension")


TagHistorySerializer = create_history_serializer(models.Tag)


class TagProfileSerializer(serializers.ModelSerializer):
    """Serializer for tag profiles."""

    tags = serializers.PrimaryKeyRelatedField(
        many=True, queryset=models.Tag.objects.all()
    )

    class Meta:
        """Serializer settings."""

        label = "Tags"
        model = User
        fields = ["id", "tags"]
        read_only_fields = ["id"]
