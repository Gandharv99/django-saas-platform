from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsCompanyAdmin(BasePermission):
    def has_permission(self, request, view):
        # Check if the user is authenticated and is a company admin
        return request.user and request.user.is_authenticated and request.user.role == 'admin'
    
class IsAdminOrSeniorMember(BasePermission):
    def has_permission(self, request, view):
        # Check if the user is authenticated and is either an admin or a senior member
        return request.user and request.user.is_authenticated and (request.user.role == 'admin' or request.user.role == 'senior_member')
    
class TaskAccessPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Read-only allowed for all authenticated users of same company
        if request.method in SAFE_METHODS:
            return obj.project.company == request.user.company

        # Members can only update their assigned tasks
        if request.user.role == 'member':
            return obj.assigned_to == request.user
        
        # Admin and senior member can modify any task
        return request.user.role in ['admin', 'senior_member']