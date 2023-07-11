"""Views of the memberships extension."""
from django.contrib.auth import get_user_model
from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.mixins import (
    CreateModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from collectivo.utils.filters import get_filterset, get_ordering_fields
from collectivo.utils.mixins import BulkEditMixin, HistoryMixin, SchemaMixin
from collectivo.utils.permissions import HasPerm, IsAuthenticated
from collectivo.utils.schema import get_choices, get_model_schema

from . import serializers
from .models import Membership, MembershipStatus, MembershipType

User = get_user_model()


class MembershipAdminViewSet(SchemaMixin, BulkEditMixin, ModelViewSet):
    """ViewSet to manage memberships with a type and status."""

    queryset = Membership.objects.all()
    serializer_class = serializers.MembershipSerializer
    permission_classes = [HasPerm]
    required_perms = {
        "GET": [("view_memberships", "memberships")],
        "ALL": [("edit_memberships", "memberships")],
    }
    filterset_class = get_filterset(serializer_class)
    ordering_fields = get_ordering_fields(serializer_class)


class MembershipProfileViewSet(SchemaMixin, ModelViewSet):
    """Manage memberships assigned to users."""

    queryset = User.objects.all()
    serializer_class = serializers.MembershipProfileSerializer
    permission_classes = [HasPerm]
    required_perms = {
        "GET": [("view_memberships", "memberships")],
        "ALL": [("edit_memberships", "memberships")],
    }
    filterset_class = get_filterset(serializers.MembershipProfileSerializer)
    ordering_fields = get_ordering_fields(
        serializers.MembershipProfileSerializer
    )


class MembershipRegisterViewset(
    CreateModelMixin, RetrieveModelMixin, GenericViewSet
):
    """ViewSet to register new memberships with additional serializers."""

    queryset = MembershipType.objects.all()
    serializer_class = serializers.MembershipRegisterCombinedSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(responses={200: OpenApiResponse()})
    @action(
        detail=True,
        url_path="schema",
        url_name="schema",
        permission_classes=[IsAuthenticated],
    )
    def _schema(self, request, pk=None):
        """Override schema to define membership type and statuses."""
        schema = get_model_schema(self)
        mtype = MembershipType.objects.get(id=pk)
        for field_name, field_obj in self.serializer_class().fields.items():
            if (
                isinstance(field_obj, Serializer)
                and field_obj.Meta.model == Membership
            ):
                fields = schema["fields"][field_name]["schema"]["fields"]
                fields["type"] = {"value": mtype.id}
                fields["status"]["choices"] = get_choices(mtype.statuses.all())

                # Add membership type data to schema for form generation
                for typefield in [
                    "has_shares",
                    "shares_number_custom",
                    "shares_number_custom_min",
                    "shares_number_custom_max",
                    "shares_number_standard",
                    "shares_number_social",
                    "shares_amount_per_share",
                    "has_fees",
                    "fees_amount_custom",
                    "fees_amount_custom_min",
                    "fees_amount_custom_max",
                    "fees_amount_standard",
                    "fees_amount_social",
                    "fees_repeat_each",
                    "fees_repeat_unit",
                    "currency",
                ]:
                    fields["type__" + typefield] = {
                        "value": getattr(mtype, typefield)
                    }

        return Response(schema)

    def retrieve(self, request, *args, **kwargs):
        """Retrieve the membership type with additional serializers."""
        instance = self.get_object()
        serializer = (
            serializers.MembershipRegisterCombinedSerializer.initialize(
                instance, request.user
            )
        )
        return Response(serializer.data)


class MembershipUserViewSet(
    SchemaMixin, ListModelMixin, UpdateModelMixin, GenericViewSet
):
    """ViewSet for users to see their own memberships."""

    queryset = Membership.objects.all()
    serializer_class = serializers.MembershipSelfSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = get_filterset(serializer_class)
    ordering_fields = get_ordering_fields(serializer_class)

    def get_queryset(self):
        """Return only the memberships of the current user."""
        return self.queryset.filter(user=self.request.user)


class MembershipTypeViewSet(SchemaMixin, ModelViewSet):
    """ViewSet to manage membership types (e.g. member of a collective)."""

    queryset = MembershipType.objects.all()
    serializer_class = serializers.MembershipTypeSerializer
    permission_classes = [HasPerm]
    required_perms = {
        "GET": [("view_memberships", "memberships")],
        "ALL": [("edit_settings", "memberships")],
    }
    filterset_class = get_filterset(serializer_class)
    ordering_fields = get_ordering_fields(serializer_class)


class MembershipStatusViewSet(SchemaMixin, ModelViewSet):
    """ViewSet to manage membership statuses (e.g. active or investing)."""

    queryset = MembershipStatus.objects.all()
    serializer_class = serializers.MembershipStatusSerializer
    permission_classes = [HasPerm]
    required_perms = {
        "GET": [("view_memberships", "memberships")],
        "ALL": [("edit_settings", "memberships")],
    }
    filterset_class = get_filterset(serializer_class)
    ordering_fields = get_ordering_fields(serializer_class)


class MembershipHistoryViewSet(
    SchemaMixin, HistoryMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    """View history of a Membership."""

    permission_classes = [HasPerm]
    required_perms = {
        "GET": [("view_memberships", "memberships")],
        "ALL": [("edit_settings", "memberships")],
    }
    serializer_class = serializers.MembershipHistorySerializer
    queryset = Membership.history.model.objects.all()
    filterset_class = get_filterset(serializers.MembershipHistorySerializer)
    ordering_fields = get_ordering_fields(
        serializers.MembershipHistorySerializer
    )


class MembershipTypeHistoryViewSet(
    SchemaMixin, HistoryMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    """View history of a Membership Type."""

    permission_classes = [HasPerm]
    required_perms = {
        "GET": [("view_memberships", "memberships")],
        "ALL": [("edit_settings", "memberships")],
    }
    serializer_class = serializers.MembershipTypeHistorySerializer
    queryset = MembershipType.history.model.objects.all()
    filterset_class = get_filterset(
        serializers.MembershipTypeHistorySerializer
    )
    ordering_fields = get_ordering_fields(
        serializers.MembershipTypeHistorySerializer
    )
