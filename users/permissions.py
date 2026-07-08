from rest_framework.permissions import BasePermission

class IsActiveAccount(BasePermission):
    message = "Your account has been deactivated."
    
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_active)


class IsVerifiedUser(BasePermission):
    message = "You must complete email or profile verification to access this."

    def has_permission(self, request, view):
        return bool(
            request.user and 
            request.user.is_authenticated and 
            getattr(request.user, 'is_verified', False)
        )


class HasRoleAdmin(BasePermission):
    message = "Access limited strictly to Administrators."

    def has_permission(self, request, view):
        role = request.auth.get('role') if request.auth else getattr(request.user, 'role', None)
        return role == 'ADMIN'


class HasRoleAgent(BasePermission):
    message = "Access limited strictly to Internal Agents."

    def has_permission(self, request, view):
        role = request.auth.get('role') if request.auth else getattr(request.user, 'role', None)
        return role == 'AGENT'


class HasRoleCustomer(BasePermission):
    def has_permission(self, request, view):
        role = request.auth.get('role') if request.auth else getattr(request.user, 'role', None)
        return role == 'CUSTOMER'