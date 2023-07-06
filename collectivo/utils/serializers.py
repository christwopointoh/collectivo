"""Serializer utilities for collectivo."""
from html import escape

from django.utils.html import format_html
from rest_framework import serializers


class UserIsPk(serializers.ModelSerializer):
    """Serializer for models with user as primary key with user id as id."""

    id = serializers.SerializerMethodField()

    def get_id(self, obj):
        """Return user id."""
        return obj.user.id


class UserFields(serializers.ModelSerializer):
    """Serializer for models with user relation with user fields as fields."""

    # Display user fields on the same level as member fields
    user__first_name = serializers.CharField(
        source="user.first_name", read_only=True, label="First name"
    )
    user__last_name = serializers.CharField(
        source="user.last_name", read_only=True, label="Last name"
    )
    user__email = serializers.EmailField(
        source="user.email", read_only=True, label="Email"
    )


def create_history_serializer(origin_model):
    """Create a serializer for the history of a model."""

    class HistorySerializer(serializers.ModelSerializer):
        """Serializer for tag history."""

        history_changed_fields = serializers.SerializerMethodField()
        history_changes = serializers.SerializerMethodField()
        history_is_latest = serializers.SerializerMethodField()

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
        def get_history_is_latest(self, obj):
            """Get boolean on whether this object is the latest."""

            if obj.next_record:
                return False
            return True

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
                        .format(
                            escape(change.field),
                            escape(change.old),
                            escape(change.new),
                        )
                    )
                return format_html(fields)
            return None

    return HistorySerializer
