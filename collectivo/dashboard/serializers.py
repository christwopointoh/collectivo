"""Serializers of the dashboard extension."""
from django.template import Context, Template
from rest_framework import serializers

from collectivo.utils.schema import Schema

from .models import DashboardTile, DashboardTileButton


class TileButtonSerializer(serializers.ModelSerializer):
    """Serializer for dashboard tile buttons."""

    class Meta:
        """Serializer settings."""

        model = DashboardTileButton
        exclude = ["name"]
        schema = {
            "fields": {
                "extension": {
                    "visible": False,
                },
                "link": {"required": True},
            }
        }


class TileSerializer(serializers.ModelSerializer):
    """Serializer for dashboard tiles."""

    class Meta:
        """Serializer settings."""

        model = DashboardTile
        exclude = ["name"]
        extra_kwargs = {
            "extension": {"read_only": True},
        }
        schema: Schema = {
            "fields": {
                "extension": {
                    "visible": False,
                },
            },
            "structure": [
                {"fields": ["label"]},
                {
                    "fields": [
                        "active",
                        "order",
                        "requires_perm",
                        "requires_not_perm",
                    ]
                },
                {"fields": ["source"]},
                {
                    "fields": [
                        "component",
                    ],
                    "visible": {
                        "field": "source",
                        "condition": "equals",
                        "value": "component",
                    },
                },
                {
                    "fields": ["content", "buttons"],
                    "visible": {
                        "field": "source",
                        "condition": "equals",
                        "value": "db",
                    },
                    "style": "col",
                },
            ],
        }


class TileDisplaySerializer(serializers.ModelSerializer):
    """Serializer to display tiles on the dashboard."""

    buttons = TileButtonSerializer(many=True, read_only=True)
    extension_name = serializers.CharField(
        source="extension.name", read_only=True
    )
    content = serializers.SerializerMethodField()

    class Meta:
        """Serializer settings."""

        model = DashboardTile
        fields = "__all__"

    def get_content(self, obj):
        """Get the content of the tile."""
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            return Template(obj.content).render(
                Context({"user": request.user})
            )
        return obj.content
