"""Permissions of the members extension."""
from rest_framework import permissions
from .models import Member


class IsNotMember(permissions.BasePermission):
    """Permission to check if user is not already a member."""

    def has_permission(self, request, view):
        """Check if user is not already a member."""
        print('Checking isnotmember')
        try:
            if request.userinfo is not None:
                l = Member.objects.filter(user_id=request.userinfo['sub'])
                print(l)
                Member.objects.get(user_id=request.userinfo['sub'])
            return False
        except Member.DoesNotExist:
            return True


class IsMembersAdmin(permissions.BasePermission):
    """Permission to check if user is an admin of this extension."""

    def has_permission(self, request, view):
        """Check if the required permission is among user roles."""
        return request.userinfo is not None and \
            'members_admin' in request.userinfo['roles']
