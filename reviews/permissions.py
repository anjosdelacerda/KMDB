from rest_framework import permissions


class ReviewCredentials(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        return (
            request.user.is_authenticated
            and request.user.is_superuser or request.user.is_critic
        )


class ReviewIdCredentials(permissions.BasePermission):
    def has_object_permission(self, request, view, userobj):
        if request.user.is_superuser:
            return True

        return request.user.is_critic and request.user == userobj
