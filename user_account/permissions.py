from rest_framework.permissions import BasePermission


class IsParticipant(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'participant'


class IsCompanyAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'companyadmin'


class IsSuperAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'superadmin'


class RoleBasedPermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated:
            return False
        if user.role in ['superadmin', 'companyadmin']:
            return True
        if user.role == 'participant':
            if view.action in ['list', 'retrieve', 'create']:
                return True
            return False
        return False

    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.role == 'superadmin':
            return True
        if user.role == 'companyadmin':
            return obj.game.company == user.company
        if user.role == 'participant':
            return obj.user == user
        return False