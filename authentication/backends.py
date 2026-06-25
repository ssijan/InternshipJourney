from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()

class EmailModelBackend(ModelBackend):
    def authenticate(self, request, username = None, password = None, **kwargs):
        login_crd = username or kwargs.get(User.USERNAME_FIELD)
        if not login_crd:
            return None
        
        try:
            user = User.objects.get(email__iexact = login_crd)
        except User.DoesNotExist:
            User().set_password(password)
            return None
        
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        
        return None 