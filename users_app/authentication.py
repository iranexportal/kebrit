from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import UntypedToken
from django.contrib.auth import get_user_model
from .models import User


class CustomJWTAuthentication(JWTAuthentication):
    """
    Custom JWT authentication that works with our User model.
    """
    
    def get_user(self, validated_token):
        """
        Attempts to find and return a user using the given validated token.
        """
        try:
            user_id = validated_token['user_id']
        except KeyError:
            raise InvalidToken('Token contained no recognizable user identification')
        
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise InvalidToken('User not found')
        
        # Note: is_active is a property that always returns True
        # since the column doesn't exist in the database
        if not getattr(user, 'is_active', True):
            raise InvalidToken('User is inactive')
        
        return user

