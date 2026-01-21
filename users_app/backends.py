from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from .models import Token


class CustomUserBackend(ModelBackend):
    """
    Custom authentication backend for our User model.
    Authenticates users by mobile number and an API token UUID.

    Note: We intentionally do NOT store passwords in our database.
    """
    
    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        Authenticate user by mobile (username) and token UUID.

        The Django admin login form only provides a "password" field, so we
        accept the token UUID in the password input for admin access.
        """
        UserModel = get_user_model()
        
        # Try to get mobile from username or kwargs
        mobile = username or kwargs.get('mobile')
        token_uuid = password or kwargs.get('token')
        if not mobile or not token_uuid:
            return None
        
        try:
            user = UserModel.objects.get(mobile=mobile)
        except UserModel.DoesNotExist:
            return None
        
        # Check API token belongs to this user
        if Token.objects.filter(uuid=token_uuid, user=user).exists():
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

