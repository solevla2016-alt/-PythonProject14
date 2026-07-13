from rest_framework.permissions import BasePermission


class IsModerator(BasePermission):
    """
    Проверяет, является ли пользователь модератором.
    """

    def has_permission(self, request, view):
        return request.user.groups.filter(name="Moderators").exists()

class IsOwner(BasePermission):
    """
    Проверяет, является ли пользователь владельцем объекта.
    """

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user

class IsModerator(BasePermission):

    def has_permission(self, request, view):
        return request.user.groups.filter(name="Moderators").exists()


class IsOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user