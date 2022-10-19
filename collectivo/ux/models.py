"""Models of the user experience module."""
from django.db import models


class MicroFrontend(models.Model):
    """A micro-frontend."""

    name = models.CharField(max_length=255, unique=True, primary_key=True)
    extension = models.ForeignKey(
        'extensions.Extension', on_delete=models.CASCADE, blank=True)
    path = models.URLField(max_length=255, blank=True)
    type = models.CharField(max_length=50, blank=True)

    def __str__(self):
        """Return string representation of the model."""
        return f'Micro-Frontend ({self.name})'
