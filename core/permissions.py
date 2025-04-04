from rest_framework.permissions import BasePermission

class IsCompanyAdmin(BasePermission):
    def has_permission(self, request, view):
        # Check if the user is authenticated and is a company admin
        return request.user and request.user.is_authenticated and request.user.role == 'admin'