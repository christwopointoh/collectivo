"""Views of the members extension."""

from . import models, serializers
from rest_framework import viewsets, mixins
from .permissions import IsMembersAdmin
from collectivo.auth.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import NotAuthenticated, PermissionDenied
from django.db.utils import IntegrityError


class MembersViewSet(
        mixins.CreateModelMixin,
        mixins.RetrieveModelMixin,
        mixins.UpdateModelMixin,
        viewsets.GenericViewSet
        ):
    """API for members to manage themselves."""

    permission_classes = [IsAuthenticated]
    queryset = models.Member.objects.all()

    def get_pk(self, request):
        """Return member id."""
        if request.userinfo is None:
            raise NotAuthenticated
        return get_object_or_404(
            self.queryset,
            user_id=request.userinfo['sub']
        ).id

    def perform_create(self, serializer):
        """Create member with user_id."""
        try:
            serializer.save(user_id=self.request.userinfo['sub'])
        except IntegrityError:
            raise PermissionDenied(detail='This user is already a member.')

    def get_object(self):
        """Return member that corresponds with current user."""
        if self.request.userinfo is None:
            raise NotAuthenticated
        return get_object_or_404(
            self.queryset,
            user_id=self.request.userinfo['sub']
        )

    def get_serializer_class(self):
        """Set name to read-only except for create."""
        if self.action == 'create':
            return serializers.MemberCreateSerializer
        return serializers.MemberSerializer


class MembersAdminViewSet(viewsets.ModelViewSet):
    """API for admins to manage members."""

    permission_classes = [IsMembersAdmin]
    serializer_class = serializers.MemberAdminSerializer
    queryset = models.Member.objects.all()
