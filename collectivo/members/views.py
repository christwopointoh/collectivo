"""Views of the members extension."""
import logging
from rest_framework import viewsets, mixins
from rest_framework.exceptions import PermissionDenied
from collectivo.auth.permissions import IsAuthenticated
from collectivo.utils import filter_lookups, get_auth_manager
from .permissions import IsMembersAdmin
from . import models, serializers
from .models import Member


member_fields = [field.name for field in models.Member._meta.get_fields()]
logger = logging.getLogger(__name__)


class MemberViewSet(
        mixins.CreateModelMixin,
        mixins.RetrieveModelMixin,
        mixins.UpdateModelMixin,
        viewsets.GenericViewSet
        ):
    """
    API for members to manage themselves.

    Create view requires authentication.
    All other views require the role 'members_user'.
    """

    queryset = models.Member.objects.all()
    permission_classes = [IsAuthenticated]

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

    def sync_user_groups(self, user_id):
        """Add user to group members after creation."""
        get_auth_manager().add_user_to_group(user_id, 'members')

    def perform_create(self, serializer):
        """Create member with user_id."""
        user_id = self.request.userinfo.user_id
        if Member.objects.filter(user_id=user_id).exists():
            raise PermissionDenied('User is already registered as a member.')
        self.sync_user_data(serializer)
        self.sync_user_groups(user_id)
        serializer.save(user_id=user_id)

    def perform_update(self, serializer):
        """Update member."""
        self.sync_user_data(serializer)
        serializer.save()

    def get_object(self):
        """Return member that corresponds with current user."""
        try:
            return self.queryset.get(user_id=self.request.userinfo.user_id)
        except Member.DoesNotExist:
            raise PermissionDenied('User is not registered as a member.')

    def get_serializer_class(self):
        """Set name to read-only except for create."""
        if self.action == 'create':
            return serializers.MemberCreateSerializer
        else:
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

    def get_serializer_class(self):
        """Set name to read-only except for create."""
        if self.action == 'list':
            return serializers.MemberAdminSerializer
        else:
            return serializers.MemberAdminDetailSerializer

    # TODO Add create/update logic here as well
