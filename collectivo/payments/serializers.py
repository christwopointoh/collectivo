"""Serializers of the payments extension."""
from rest_framework import serializers

from collectivo.utils.serializers import UserIsPk

from . import models


class PaymentProfileSerializer(UserIsPk):
    """Serializer for payment profiles."""

    class Meta:
        """Serializer settings."""

        model = models.PaymentProfile
        fields = "__all__"
        read_only_fields = ["user"]


class PaymentSerializer(serializers.ModelSerializer):
    """Serializer for payments."""

    class Meta:
        """Serializer settings."""

        model = models.Payment
        fields = "__all__"


class SubscriptionSerializer(serializers.ModelSerializer):
    """Serializer for subscriptions."""

    class Meta:
        """Serializer settings."""

        model = models.Subscription
        fields = "__all__"
