"""Views of the emails module."""
from django.contrib.auth import get_user_model
from rest_framework import mixins, viewsets

from collectivo.utils.filters import get_filterset, get_ordering_fields
from collectivo.utils.mixins import HistoryMixin, SchemaMixin
from collectivo.utils.permissions import HasPerm

from . import models, serializers

User = get_user_model()


class EmailProfileViewSet(SchemaMixin, viewsets.ModelViewSet):
    """Manage emails assigned to users."""

    queryset = User.objects.all()
    serializer_class = serializers.EmailProfileSerializer
    permission_classes = [HasPerm]
    required_perms = {
        "GET": [("view_emails", "core")],
        "ALL": [("edit_emails", "core")],
    }
    filterset_class = get_filterset(serializers.EmailProfileSerializer)
    ordering_fields = get_ordering_fields(serializers.EmailProfileSerializer)


class EmailDesignViewSet(SchemaMixin, viewsets.ModelViewSet):
    """Manage email designs."""

    permission_classes = [HasPerm]
    required_perms = {
        "GET": [("view_emails", "emails")],
        "ALL": [("edit_emails", "emails")],
    }
    serializer_class = serializers.EmailDesignSerializer
    filterset_class = get_filterset(serializers.EmailDesignSerializer)
    ordering_fields = get_ordering_fields(serializers.EmailDesignSerializer)
    queryset = models.EmailDesign.objects.all()


class EmailTemplateViewSet(SchemaMixin, viewsets.ModelViewSet):
    """Manage email templates."""

    permission_classes = [HasPerm]
    required_perms = {
        "GET": [("view_emails", "emails")],
        "ALL": [("edit_emails", "emails")],
    }
    serializer_class = serializers.EmailTemplateSerializer
    filterset_class = get_filterset(serializers.EmailTemplateSerializer)
    ordering_fields = get_ordering_fields(serializers.EmailTemplateSerializer)
    queryset = models.EmailTemplate.objects.all()


class EmailCampaignViewSet(SchemaMixin, viewsets.ModelViewSet):
    """Manage email campaigns (mass email orders)."""

    permission_classes = [HasPerm]
    required_perms = {
        "GET": [("view_emails", "emails")],
        "ALL": [("edit_emails", "emails")],
    }
    serializer_class = serializers.EmailCampaignSerializer
    filterset_class = get_filterset(serializers.EmailCampaignSerializer)
    ordering_fields = get_ordering_fields(serializers.EmailCampaignSerializer)
    queryset = models.EmailCampaign.objects.all()


class EmailAutomationViewSet(
    SchemaMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    """Manage email automations (mass email orders)."""

    permission_classes = [HasPerm]
    required_perms = {
        "GET": [("view_emails", "emails")],
        "ALL": [("edit_emails", "emails")],
    }
    serializer_class = serializers.EmailAutomationSerializer
    filterset_class = get_filterset(serializers.EmailAutomationSerializer)
    ordering_fields = get_ordering_fields(
        serializers.EmailAutomationSerializer
    )
    queryset = models.EmailAutomation.objects.all()


class EmailAutomationHistoryViewSet(
    SchemaMixin, HistoryMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    """View EmailAutomation history."""

    permission_classes = [HasPerm]
    required_perms = {
        "GET": [("view_emails", "emails")],
        "ALL": [("edit_emails", "emails")],
    }
    serializer_class = serializers.EmailAutomationHistorySerializer
    filterset_class = get_filterset(
        serializers.EmailAutomationHistorySerializer
    )
    ordering_fields = get_ordering_fields(
        serializers.EmailAutomationHistorySerializer
    )
    queryset = models.EmailAutomation.objects.all()


class EmailDesignHistoryViewSet(
    SchemaMixin, HistoryMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    """View EmailDesign history."""

    permission_classes = [HasPerm]
    required_perms = {
        "GET": [("view_emails", "emails")],
        "ALL": [("edit_emails", "emails")],
    }
    serializer_class = serializers.EmailDesignHistorySerializer
    filterset_class = get_filterset(serializers.EmailDesignHistorySerializer)
    ordering_fields = get_ordering_fields(
        serializers.EmailDesignHistorySerializer
    )
    queryset = models.EmailDesign.objects.all()


class EmailCampaignHistoryViewSet(
    SchemaMixin, HistoryMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    """View EmailCampaign history."""

    permission_classes = [HasPerm]
    required_perms = {
        "GET": [("view_emails", "emails")],
        "ALL": [("edit_emails", "emails")],
    }
    serializer_class = serializers.EmailCampaignHistorySerializer
    filterset_class = get_filterset(serializers.EmailCampaignHistorySerializer)
    ordering_fields = get_ordering_fields(
        serializers.EmailCampaignHistorySerializer
    )
    queryset = models.EmailCampaign.objects.all()


class EmailTemplateHistoryViewSet(
    SchemaMixin, HistoryMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    """View EmailTemplate history."""

    permission_classes = [HasPerm]
    required_perms = {
        "GET": [("view_emails", "emails")],
        "ALL": [("edit_emails", "emails")],
    }
    serializer_class = serializers.EmailTemplateHistorySerializer
    filterset_class = get_filterset(serializers.EmailTemplateHistorySerializer)
    ordering_fields = get_ordering_fields(
        serializers.EmailTemplateHistorySerializer
    )
    queryset = models.EmailTemplate.objects.all()
