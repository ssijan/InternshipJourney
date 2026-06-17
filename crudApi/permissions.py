from rest_framework.permissions import BasePermission
from .models import Account, Transaction
 
class IsAccountOwner(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Account):
            return obj.owner == request.user
        if isinstance(obj, Transaction):
            return obj.account.owner == request.user
        return False