from rest_framework.permissions import BasePermission


class IsModerator(BasePermission):
    """Проверяет, является ли пользователь модератором."""

    def has_permission(self, request, view):
        return request.user.groups.filter(
            name="Moderators"
        ).exists()

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)