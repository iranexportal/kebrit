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
        # Try to get login identifier from username field
        login_username = username or kwargs.get('username') or kwargs.get('mobile')
        token_uuid = password or kwargs.get('token')
        if not token_uuid:
            return None

        # Use token to uniquely identify the user (mobile is no longer globally unique)
        token_obj = Token.objects.select_related('user').filter(uuid=token_uuid).first()
        if not token_obj:
            return None

        user = token_obj.user
        if login_username:
            # If user has a username, admin must login with it
            if getattr(user, 'username', None):
                if user.username != login_username:
                    return None
            else:
                # Fallback for legacy rows without username set
                if user.mobile != login_username:
                    return None

        return user
        
        # unreachable
    
    def get_user(self, user_id):
        """
        Retrieve user by ID.
        """
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None

