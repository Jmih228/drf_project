from rest_framework.permissions import BasePermission


class IsNotStaff(BasePermission):
    def has_permission(self, request, view):
        if not request.user.groups.filter(name='staff').exists():
            return True
        return False


class IsOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.user == obj.owner
