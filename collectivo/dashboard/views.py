"""Views of the dashboard extension."""
from django.db.models import Q
from rest_framework import viewsets
from collectivo.auth.permissions import IsCollectivoAdmin, IsAuthenticated
from . import models, serializers


class DashboardTileViewSet(viewsets.ModelViewSet):
    """Manage dashboard tiles."""

    def get_queryset(self):
        """Show only items where user has required roles."""
        user_roles = self.request.userinfo.roles

        queryset = models.DashboardTile.objects.filter(
            Q(required_role__in=user_roles) |
            Q(required_role=None),
            ~Q(blocked_role__in=user_roles)
        )
        return queryset

    def get_permissions(self):
        """Set permissions for this viewset."""
        if self.action == 'list':
            return [IsAuthenticated()]
        return [IsCollectivoAdmin()]

    def get_serializer_class(self):
        """Set name to read-only except for create."""
        if self.request.method == 'POST':
            return serializers.DashboardTileCreateSerializer
        return serializers.DashboardTileSerializer
