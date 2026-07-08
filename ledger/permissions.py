from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsTransactionOwnerOrStaff(BasePermission):
    message = "Object Access Denied: You do not own this transaction."

    def has_object_permission(self, request, view, obj):
        # Extract metadata from token claims payload or db fallback
        role = request.auth.get('role') if request.auth else getattr(request.user, 'role', None)
        
        if role in ['ADMIN', 'AGENT']:
            return True
            
        # Hard ownership validation constraint against row object
        return obj.user == request.user