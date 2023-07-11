"""Utilities for collectivo models."""

from rest_framework import serializers


class SingleInstance:
    """Mixin for models that should only have one instance."""

    @classmethod
    def object(cls, check_valid=False):
        """Get or create instance."""
        if not cls.objects.exists():
            obj = cls.objects.create()
        else:
            obj = cls.objects.first()
        if check_valid:
            obj.is_valid()
        return obj

    def is_valid(self):
        """Check if object is valid."""

        class TempSerializer(serializers.ModelSerializer):
            """Serializer to check if object is valid."""

            class Meta:
                """Meta class."""

                model = self.__class__
                fields = "__all__"

        temp_serializer = TempSerializer(data=TempSerializer(self).data)
        temp_serializer.is_valid(raise_exception=True)

    def save(self, *args, **kwargs):
        """Save object or raise exception if an instance already exists."""
        if self.pk is None and self.__class__.objects.exists():
            raise Exception("Only one instance of this model allowed.")
        super().save(*args, **kwargs)


class NameLabelModel:
    """Mixin for models with name and label fields."""

    def __str__(self):
        """Return the string representation."""
        name = self.label if self.label else self.name
        if self.extension:
            return f"{self.extension.label}: {name}"
        return name

    def save(self, *args, **kwargs):
        """Set name to be the same as label if no name is given."""
        if not self.name:
            self.name = self.label.replace(" ", "_").lower()
        if not self.label:
            self.label = self.name.replace("_", " ").capitalize()
        super().save(*args, **kwargs)
