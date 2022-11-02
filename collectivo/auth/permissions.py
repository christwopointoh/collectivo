"""Permissions of the keycloak module to be used in DRF views."""
from rest_framework import permissions


class IsAuthenticated(permissions.BasePermission):
    """Permission to check if user is authenticated."""

    def has_permission(self, request, view):
        """Check if user is authenticated."""
        return request.is_authenticated


class IsCollectivoAdmin(permissions.BasePermission):
    """Permission to check if user has the role 'is_collectivo_admin'."""

    def has_permission(self, request, view):
        """Check if user is authenticated."""
        return hasattr(request, 'userinfo') and \
            'is_collectivo_admin' in request.userinfo['roles']
