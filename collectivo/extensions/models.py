"""Models of the extension module."""
from django.db import models


class Extension(models.Model):
    """An extension that can dynamically be added to collectivo."""

    name = models.CharField(max_length=255, unique=True, primary_key=True)
    version = models.CharField(max_length=50, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        """Return string representation of the model."""
        return f'Extension ({self.name})'
