from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model


class CustomUserBackend(ModelBackend):
    """
    Custom authentication backend for our User model.
    Authenticates users by mobile number and plain text password.
    """
    
    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        Authenticate user by mobile (username) and password.
        """
        UserModel = get_user_model()
        
        # Try to get mobile from username or kwargs
        mobile = username or kwargs.get('mobile')
        if not mobile:
            return None
        
        try:
            user = UserModel.objects.get(mobile=mobile)
        except UserModel.DoesNotExist:
            return None
        
        # Check password (plain text comparison)
        if user.check_password(password):
            return user
        
        return None
    
    def get_user(self, user_id):
        """
        Retrieve user by ID.
        """
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None

