"""Views of the members extension."""

from django.db.utils import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins
from rest_framework.exceptions import NotAuthenticated, PermissionDenied

from collectivo.utils import filter_lookups
from .permissions import IsMembersAdmin, IsMembersUser
from . import models, serializers


member_fields = [field.name for field in models.Member._meta.get_fields()]


class MemberViewSet(
        mixins.CreateModelMixin,
        mixins.RetrieveModelMixin,
        mixins.UpdateModelMixin,
        viewsets.GenericViewSet
        ):
    """
    API for members to manage themselves.

    Requires the role 'members_user'.
    """

    permission_classes = [IsMembersUser]
    queryset = models.Member.objects.all()

    def get_pk(self, request):
        """Return member id."""
        if request.userinfo is None:
            raise NotAuthenticated
        return get_object_or_404(
            self.queryset,
            user_id=request.userinfo['sub']  # TODO Loose coupling
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
            user_id=self.request.userinfo['sub']  # TODO Loose coupling
        )

    def get_serializer_class(self):
        """Set name to read-only except for create."""
        if self.action == 'create':
            return serializers.MemberCreateSerializer
        return serializers.MemberSerializer


class MembersAdminViewSet(viewsets.ModelViewSet):
    """
    API for admins to manage members.

    Requires the role 'members_admin'.
    """

    queryset = models.Member.objects.all()
    serializer_class = serializers.MemberAdminSerializer

    filterset_fields = {field: filter_lookups for field in member_fields}
    ordering_fields = member_fields

    permission_classes = [IsMembersAdmin]
