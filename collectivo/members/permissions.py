"""Permissions of the members extension."""
from rest_framework import permissions


class IsMembersUser(permissions.BasePermission):
    """Permission to check if user has access to this extension."""

    def has_permission(self, request, view):
        """Check if the required permission is among user roles."""
        try:
            print("Checking permission, userinfo is: ", request.userinfo)
            return 'members_user' in request.userinfo['roles']
        except Exception:
            return False


class IsMembersAdmin(permissions.BasePermission):
    """Permission to check if user has admin access to this extension."""

    def has_permission(self, request, view):
        """Check if the required permission is among user roles."""
        try:
            print("Checking permission, userinfo is: ", request.userinfo)
            return 'members_admin' in request.userinfo['roles']
        except Exception:
            return False
