"""Views of the profiles extension."""
from rest_framework import mixins, viewsets

from collectivo.utils.filters import get_filterset, get_ordering_fields
from collectivo.utils.mixins import HistoryMixin, SchemaMixin, SelfMixin
from collectivo.utils.permissions import (
    HasPerm,
    IsAuthenticated,
    ReadOrIsSuperuser,
)
from collectivo.utils.viewsets import SingleModelViewSet

from . import models, serializers
from .models import ProfileSettings, UserProfile


class ProfileSettingsViewSet(SingleModelViewSet):
    """Viewset for core settings."""

    queryset = ProfileSettings.objects.all()
    serializer_class = serializers.ProfileSettingsSerializer
    permission_classes = [ReadOrIsSuperuser]


class ProfileUserViewSet(
    SelfMixin,
    SchemaMixin,
    viewsets.GenericViewSet,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
):
    """ViewSet for users to manage their own profile."""

    queryset = UserProfile.objects.all()
    serializer_class = serializers.ProfileUserSerializer
    permission_classes = [IsAuthenticated]


class ProfileAdminViewSet(
    SchemaMixin,
    viewsets.GenericViewSet,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
):
    """ViewSet for admins to manage user profiles."""

    queryset = UserProfile.objects.all()
    serializer_class = serializers.ProfileAdminSerializer
    permission_classes = [HasPerm]
    required_perms = {
        "GET": [("view_users", "core")],
        "ALL": [("edit_users", "core")],
    }
    filterset_class = get_filterset(serializers.ProfileAdminSerializer)
    ordering_fields = get_ordering_fields(serializers.ProfileAdminSerializer)


class ProfileHistoryViewSet(
    SchemaMixin, HistoryMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    """View history of a Profile."""

    permission_classes = [HasPerm]
    required_perms = {
        "GET": [("view_users", "core")],
        "ALL": [("edit_users", "core")],
    }
    serializer_class = serializers.ProfileHistorySerializer
    queryset = models.UserProfile.history.model.objects.all()
    filterset_class = get_filterset(serializers.ProfileHistorySerializer)
    ordering_fields = get_ordering_fields(serializers.ProfileHistorySerializer)
