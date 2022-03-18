from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS

from users.models import User


class AdminPermissionOne(permissions.BasePermission):
    message = 'This operation is available only to the Admin.'

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and request.user.role == User.ADMIN


class AdminPermissionList(permissions.BasePermission):
    message = 'This operation is available only to the Admin.'

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == User.ADMIN


class ModeratorPermissionOne(permissions.BasePermission):
    message = 'This operation is available only to the Moderator.'

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and request.user.role == User.MODERATOR


class ModeratorPermissionList(permissions.BasePermission):
    message = 'This operation is available only to the Moderator.'

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == User.MODERATOR


class OwnerPermissionOne(permissions.BasePermission):
    message = 'This operation is available only to the Owner.'

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and obj.user == request.user


class OwnerUserPermissionOne(permissions.BasePermission):
    """For User model only"""
    message = 'This operation is available only to the Owner.'

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and obj.id == request.user.id


class OwnerOrModerPermissionOne(permissions.BasePermission):
    message = 'This operation is available only to Owner or Moderator or Admin.'

    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_authenticated and (
                obj.user == request.user or
                request.user.role == User.ADMIN or
                request.user.role == User.MODERATOR
            )
        )


class ReadOnlyOrAdminPermissionList(permissions.BasePermission):
    """
    The request is authenticated as admin, or is a read-only request.
    """
    message = 'This operation is available only to the Admin.'

    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS or
            request.user.is_authenticated and
            request.user.role == User.ADMIN
        )
