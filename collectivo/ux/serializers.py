"""Serializers of the collectivo ux extension."""
from rest_framework import serializers


class MenuItemSerializer(serializers.Serializer):
    """Serializer of the MenuItem class."""

    # TODO For subitems
    # albums = serializers.ListSerializer(child=AlbumSerializer(),
    # source='album_set')

    display = serializers.CharField()
    path = serializers.CharField()
    # TODO Extend with other attributes
