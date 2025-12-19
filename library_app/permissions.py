from rest_framework.permissions import BasePermission


class IsSuperUser(BasePermission):
    """Permission class for admin-only endpoints"""
    
    def has_permission(self, request, view):
        return request.user and request.user.is_superuser
