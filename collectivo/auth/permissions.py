"""Permissions of the keycloak module to be used in DRF views."""
from rest_framework import permissions


class IsAuthenticated(permissions.BasePermission):
    """Permission to check if user is authenticated."""

    def has_permission(self, request, view):
        """Check if user is authenticated."""
        return request.userinfo is not None


class IsSelf(permissions.BasePermission):
    """Permission to check if the object has the user's id."""

    def has_object_permission(self, request, view, obj):
        """Check if the object has the user's id."""
        print('Checking IsSelf Permission')
        return request.userinfo is not None and \
            request.userinfo['sub'] == obj.user_id
