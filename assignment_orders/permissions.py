from rest_framework import permissions


class IsAdminOrMe(permissions.BasePermission):
    """
    Permission to get own data by user or admin
    """
    message = "You don't have enough access"

    def has_object_permission(self, request, view, obj):
        return request.user.id == obj.id or request.user.is_staff

