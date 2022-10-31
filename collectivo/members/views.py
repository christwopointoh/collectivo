"""Views of the members extension."""

from . import models, serializers
from rest_framework import viewsets, mixins
from .permissions import IsNotMember, IsMembersAdmin
from collectivo.auth.permissions import IsAuthenticated, IsSelf
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from django.http import Http404
from rest_framework.exceptions import NotAuthenticated, PermissionDenied
from django.db.utils import IntegrityError


class MembersViewSet(
        mixins.CreateModelMixin,
        mixins.RetrieveModelMixin,
        mixins.UpdateModelMixin,
        viewsets.GenericViewSet
    ):
    """API for members to manage themselves."""

    queryset = models.Member.objects.all()

    def get_pk(self, request):
        if request.userinfo is None:
            raise NotAuthenticated
        return get_object_or_404(
            self.queryset,
            user_id=request.userinfo['sub']
        ).id

    def perform_create(self, serializer):
        try :
            serializer.save(user_id=self.request.userinfo['sub'])
        except IntegrityError:
            raise PermissionDenied(detail='This user is already a member.')

    def get_object(self):
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

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsSelf]
        return [permission() for permission in permission_classes]


class MembersAdminViewSet(viewsets.ModelViewSet):
    """API for admins to manage members."""

    permission_classes = [IsMembersAdmin]

    queryset = models.Member.objects.all()

    def get_serializer_class(self):
        return serializers.MemberAdminSerializer
