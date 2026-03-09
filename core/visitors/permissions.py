from rest_framework.permissions import BasePermission

class IsDeskOfficer(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        return request.user.groups.filter(name="Desk Officer").exists()