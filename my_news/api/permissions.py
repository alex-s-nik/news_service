from rest_framework import permissions

from users.models import User


class ReadAnonCreateAuthUpdateAdminOrAuthor(permissions.BasePermission):
    """Список новостей и конкретную новость может получить любой пользователь, в том числе
    незарегистрированный.
    Создать новость может только зарегистрированный пользователь.
    Редактировать и удалять новости может только автор этой новости или администратор."""
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return True
        return request.user == obj.author or request.user.role == User.ADMIN_ROLE
