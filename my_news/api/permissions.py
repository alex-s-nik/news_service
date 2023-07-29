from rest_framework import permissions

from users.models import User


class ReadAnonCreateAuthUpdateAdminOrAuthor(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return True
        return request.user == obj.author or request.user.role == User.ADMIN_ROLE
