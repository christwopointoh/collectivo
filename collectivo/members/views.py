"""Views of the members extension."""
import logging
from rest_framework import viewsets, mixins
from rest_framework.exceptions import PermissionDenied
from collectivo.auth.permissions import IsAuthenticated
from collectivo.utils import get_auth_manager
from collectivo.views import SchemaMixin
from .permissions import IsMembersAdmin
from . import models, serializers
from .models import Member
from django.utils.timezone import localdate


logger = logging.getLogger(__name__)

member_fields = [field.name for field in models.Member._meta.get_fields()]

filterset_fields = {
    'first_name': ('contains', ),
    'last_name': ('contains', ),
    'person_type': ('exact', ),
    'membership_status': ('exact', ),
}


class MemberAuthSyncMixin:
    """Functions to sync user data with auth manager."""

    def sync_user_data(self, serializer):
        """Update user data if it has changed."""
        auth_manager = get_auth_manager()
        user_fields = auth_manager.get_user_fields()
        old_user_data = self.request.userinfo
        user_id = old_user_data.user_id
        if user_id is None:
            return
        new_user_data = {
            k: v for k, v in serializer.validated_data.items()
            if k in user_fields
        }
        user_fields_have_changed = any([
            new_user_data.get(field) != getattr(old_user_data, field)
            for field in new_user_data.keys()
        ])
        if user_fields_have_changed:
            auth_manager.update_user(user_id=user_id, **new_user_data)

    def sync_user_roles(self, user_id):
        """Add user to group members after creation."""
        role = 'members_user'
        auth_manager = get_auth_manager()
        role_id = auth_manager.get_realm_role(role)['id']
        auth_manager.assign_realm_roles(
            user_id, {'id': role_id, 'name': role})


class GenericMemberViewSet(
        SchemaMixin,
        MemberAuthSyncMixin,
        viewsets.GenericViewSet):
    """Base class for all member views."""

    queryset = models.Member.objects.all()

    def _perform_create(self, user_id, serializer):
        """Create member with user_id."""
        if Member.objects.filter(user_id=user_id).exists():
            raise PermissionDenied('User is already registered as a member.')
        self.sync_user_data(serializer)
        self.sync_user_roles(user_id)
        extra_fields = {
            'user_id': user_id,
            'membership_start': localdate(),
        }
        if 'tags' in serializer.validated_data:
            extra_fields['tags'] = serializer.validated_data['tags']
        serializer.save(**extra_fields)

    def perform_update(self, serializer):
        """Update member."""
        self.sync_user_data(serializer)
        self.sync_user_roles(serializer.initial_data['user_id'])
        serializer.save()


class MemberRegisterView(mixins.CreateModelMixin, GenericMemberViewSet):
    """
    API for members to register themselves.

    Requires authentication.
    """

    serializer_class = serializers.MemberRegisterSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """Create member with user_id from keycloak."""
        user_id = self.request.userinfo.user_id
        self._perform_create(user_id, serializer)


class MemberViewSet(
        mixins.RetrieveModelMixin,
        mixins.UpdateModelMixin,
        GenericMemberViewSet
        ):
    """
    API for members to manage themselves.

    Requires authentication and registration.
    """

    serializer_class = serializers.MemberProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """Return member that corresponds with current user."""
        try:
            return self.queryset.get(user_id=self.request.userinfo.user_id)
        except Member.DoesNotExist:
            raise PermissionDenied('User is not registered as a member.')


class MembersAdminSummaryView(mixins.ListModelMixin, GenericMemberViewSet):
    """
    API for admins to get a summary of members.

    Requires the role 'members_admin'.
    """

    serializer_class = serializers.MemberSummarySerializer
    permission_classes = [IsMembersAdmin]
    filterset_fields = filterset_fields
    ordering_fields = member_fields


class MembersAdminViewSet(viewsets.ModelViewSet, GenericMemberViewSet):
    """
    API for admins to manage members.

    Requires the role 'members_admin'.
    """

    serializer_class = serializers.MemberAdminSerializer
    permission_classes = [IsMembersAdmin]
    filterset_fields = filterset_fields
    ordering_fields = member_fields

    def perform_create(self, serializer):
        """Create member with user_id."""
        if 'user_id' in serializer.initial_data:
            user_id = serializer.initial_data['user_id']
        else:
            user_id = None
        if user_id is None:
            serializer.save()
            return
        self._perform_create(user_id, serializer)


class MemberTagViewSet(viewsets.ModelViewSet):
    """Manage member tags."""

    permission_classes = [IsMembersAdmin]
    queryset = models.MemberTag.objects.all()

    def get_serializer_class(self):
        """Set name to read-only except for create."""
        if self.request.method == 'POST':
            return serializers.MemberTagCreateSerializer
        return serializers.MemberTagSerializer
