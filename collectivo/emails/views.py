"""Views of the emails module."""
from django.contrib.auth import get_user_model
from rest_framework import viewsets

from collectivo.utils.filters import get_filterset, get_ordering_fields
from collectivo.utils.mixins import SchemaMixin
from collectivo.utils.permissions import IsSuperuser

from . import models, serializers

User = get_user_model()


class EmailProfileViewSet(SchemaMixin, viewsets.ModelViewSet):
    """Manage emails assigned to users."""

    queryset = User.objects.all()
    serializer_class = serializers.EmailProfileSerializer
    permission_classes = [IsSuperuser]
    filterset_class = get_filterset(serializers.EmailProfileSerializer)
    ordering_fields = get_ordering_fields(serializers.EmailProfileSerializer)


class EmailDesignViewSet(SchemaMixin, viewsets.ModelViewSet):
    """Manage email designs."""

    permission_classes = [IsSuperuser]
    serializer_class = serializers.EmailDesignSerializer
    filterset_class = get_filterset(serializers.EmailDesignSerializer)
    ordering_fields = get_ordering_fields(serializers.EmailProfileSerializer)
    queryset = models.EmailDesign.objects.all()


class EmailTemplateViewSet(SchemaMixin, viewsets.ModelViewSet):
    """Manage email templates."""

    permission_classes = [IsSuperuser]
    serializer_class = serializers.EmailTemplateSerializer
    filterset_class = get_filterset(serializers.EmailTemplateSerializer)
    ordering_fields = get_ordering_fields(serializers.EmailProfileSerializer)
    queryset = models.EmailTemplate.objects.all()


class EmailCampaignViewSet(SchemaMixin, viewsets.ModelViewSet):
    """Manage email campaigns (mass email orders)."""

    permission_classes = [IsSuperuser]
    serializer_class = serializers.EmailCampaignSerializer
    filterset_class = get_filterset(serializers.EmailCampaignSerializer)
    ordering_fields = get_ordering_fields(serializers.EmailProfileSerializer)
    queryset = models.EmailCampaign.objects.all()
