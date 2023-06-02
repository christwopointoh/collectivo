"""Views of the components module."""
from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet

from collectivo.utils.mixins import SchemaMixin
from collectivo.utils.permissions import ReadOrIsSuperuser

from .models import Component
from .serializers import ComponentSerializer


class ComponentViewSet(SchemaMixin, ListModelMixin, GenericViewSet):
    """Manage components."""

    queryset = Component.objects.all()
    serializer_class = ComponentSerializer
    permission_classes = [ReadOrIsSuperuser]
