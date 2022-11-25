from ipdb import set_trace
from rest_framework import permissions


class IsUserAdm(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.is_superuser:
            return True


class IsUserCritic(permissions.BasePermission):
    def has_permission(self, request, view):
        
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.user.is_critic and obj.id == request.user.id:
            print(obj)
            return True
        return False
