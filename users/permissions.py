from rest_framework import permissions
from users.models import User


class AdminPermission(permissions.BasePermission):
    message = 'This operation is available only to the Admin.'

    def has_permission(self, request, view):
        return request.user.role == User.ADMIN


class ModeratorPermission(permissions.BasePermission):
    message = 'This operation is available only to Moderator or Admin.'

    def has_permission(self, request, view):
        return request.user.role == User.MODERATOR


class OwnerPermission(permissions.BasePermission):
    message = 'This operation is available only to Owner or Moderator or Admin.'

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class EditPermission(permissions.BasePermission):
    message = 'This operation is available only to Owner or Moderator or Admin.'

    def has_object_permission(self, request, view, obj):
        if (obj.user == request.user) | (request.user.role == User.ADMIN) | (request.user.role == User.MODERATOR):
            return True
        return False
