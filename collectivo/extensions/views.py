"""Views of the extensions module."""
from rest_framework import viewsets
from .models import Extension
from .serializers import ExtensionSerializer, ExtensionCreateSerializer


class ExtensionViewSet(viewsets.ModelViewSet):
    """Manage extensions."""

    queryset = Extension.objects.all()

    def get_serializer_class(self):
        """Set name to read-only except for create."""
        if self.request.method == 'POST':
            return ExtensionCreateSerializer
        return ExtensionSerializer
