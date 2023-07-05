"""Serializers of the tags extension."""
from django.contrib.auth import get_user_model
from django.utils.html import format_html
from rest_framework import serializers

from . import models

User = get_user_model()


class TagSerializer(serializers.ModelSerializer):
    """Serializer for tags."""

    class Meta:
        """Serializer settings."""

        model = models.Tag
        fields = "__all__"
        read_only_fields = ("id", "extension")


def create_history_serializer(origin_model):
    """Create a serializer for the history of a model."""

    class HistorySerializer(serializers.ModelSerializer):
        """Serializer for tag history."""

        history_changed_fields = serializers.SerializerMethodField()
        history_changes = serializers.SerializerMethodField()

        class Meta:
            """Serializer settings."""

            model = origin_model.history.model
            fields = "__all__"
            schema = {
                "fields": {
                    "history_changes": {
                        "input_type": "display_html",
                    }
                }
            }

        # Methods from https://stackoverflow.com/a/72187314/14396787

        def get_history_changed_fields(self, obj):
            """Get changed fields."""

            if obj.prev_record:
                delta = obj.diff_against(obj.prev_record)
                return delta.changed_fields
            return None

        def get_history_changes(self, obj):
            """Get changes."""

            fields = ""
            if obj.prev_record:
                delta = obj.diff_against(obj.prev_record)

                for change in delta.changes:
                    fields += str(
                        "<strong>{}</strong> changed from <span"
                        " style='background-color:#ffb5ad'>{}</span> to <span"
                        " style='background-color:#b3f7ab'>{}</span> . <br/>"
                        .format(change.field, change.old, change.new)
                    )
                return format_html(fields)
            return None

    return HistorySerializer


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
