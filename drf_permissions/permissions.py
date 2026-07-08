from rest_framework.permissions import BasePermission, SAFE_METHODS, DjangoObjectPermissions


class IsStaffUser(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_staff)
    

class IsAccountOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if not (request.user and request.user.is_authenticated):
            return False
        return  obj.user == request.user
    
class IsVerifiedUser(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and getattr(request.user,'is_verified',False))
    
class IsActiveAccount(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_active)
    

class HasRoleAdmin(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and 
            request.user.is_authenticated and 
            getattr(request.user, 'role', None) == 'ADMIN'
        )
    
class HasRoleAgent(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user and 
            request.user.is_authenticated and
            getattr(request.user, 'role', None) == 'AGENT'
        )
    

class IsTransactionOwnerOrStaff(BasePermission):
    message = "You do not have authorization to view this transaction record."

    def has_object_permission(self, request, view, obj):
        user_ob = request.auth.get('role') if request.auth else getattr(request.user, 'role', None)
        if user_ob in ['ADMIN', 'AGENT']:
            return True

        return obj.user == request.user
    



class GuardianObjectPermissions(DjangoObjectPermissions):
    perms_map = {
        'GET': ['%(app_label)s.view_%(model_name)s'],
        'OPTIONS': [],
        'HEAD': [],
        'POST': ['%(app_label)s.add_%(model_name)s'],
        'PUT': ['%(app_label)s.edit_%(model_name)s'],
        'PATCH': ['%(app_label)s.edit_%(model_name)s'],
        'DELETE': ['%(app_label)s.delete_%(model_name)s'],
    }