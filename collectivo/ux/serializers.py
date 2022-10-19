"""Serializers of the collectivo user experience module."""
from rest_framework import serializers
from .models import MicroFrontend


class MenuItemSerializer(serializers.Serializer):
    """Serializer of the MenuItem class."""

    # TODO For subitems
    # albums = serializers.ListSerializer(child=AlbumSerializer(),
    # source='album_set')

    display = serializers.CharField()
    path = serializers.CharField()
    # TODO Extend with other attributes


class MicroFrontendCreateSerializer(serializers.ModelSerializer):
    """Serializer to create new microfrontend objects."""

    class Meta:
        """Serializer settings."""

        model = MicroFrontend
        fields = '__all__'


class MicroFrontendSerializer(serializers.ModelSerializer):
    """Serializer for existing microfrontend objects."""

    class Meta:
        """
        Serializer settings.

        The name cannot be changed because it is the primary key to identify
        the extension. A new extension has to be created to set a new name.
        """

        model = MicroFrontend
        fields = '__all__'
        read_only_fields = ('name', )
