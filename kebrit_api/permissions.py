from rest_framework import permissions


class IsClientTokenAuthenticated(permissions.BasePermission):
    """
    Permission for endpoints that require a valid customer token.
    """

    message = "Client token required"

    def has_permission(self, request, view):
        return bool(getattr(request, "auth_company", None))

