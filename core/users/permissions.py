from rest_framework.permissions import BasePermission

class IsDeskOfficer(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "STAFF"

class IsSupervisor(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "SUPERVISOR"

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "ADMIN"
