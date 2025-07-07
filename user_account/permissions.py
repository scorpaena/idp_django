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


# class RoleBasedPermission(BasePermission):
#     def has_permission(self, request, view):
#         user = request.user
#         if not user.is_authenticated:
#             return False
#         if user.role in ['superadmin', 'companyadmin']:
#             return True
#         if user.role == 'participant':
#             if view.action in ['list', 'retrieve', 'create']:
#                 return True
#             return False
#         return False
#
#     def has_object_permission(self, request, view, obj):
#         user = request.user
#         if user.role == 'superadmin':
#             return True
#         if user.role == 'companyadmin':
#             return obj.user.company == user.company
#         if user.role == 'participant':
#             return obj.user == user
#         return False


class RoleBasedPermission(BasePermission):
    """
    A flexible permission class that:
    - allows superadmins everything
    - allows companyadmins for their company
    - allows participants for their own objects
    """

    # the path to follow to find the user from the object
    # e.g. "user" for GameSession
    #      "session.user" for GameResult
    user_path = "user"

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
            target_user = self._resolve_user(obj)
            return target_user and target_user.company == user.company
        if user.role == 'participant':
            target_user = self._resolve_user(obj)
            return target_user == user
        return False

    def _resolve_user(self, obj):
        """
        Follow the user_path string to dynamically resolve the user
        """
        path_parts = self.user_path.split(".")
        target = obj
        for part in path_parts:
            target = getattr(target, part, None)
            if target is None:
                return None
        return target


class GameSessionPermission(RoleBasedPermission):
    ...


class GameResultPermission(RoleBasedPermission):
    user_path = "session.user"
