from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import UntypedToken
from django.contrib.auth import get_user_model
from django.conf import settings
from .models import User


class CustomJWTAuthentication(JWTAuthentication):
    """
    Custom JWT authentication that works with our User model.
    Supports both cookie-based and header-based token authentication.
    """
    
    def get_header(self, request):
        """
        Extracts the header containing the JSON web token from the given
        request. Also checks cookies as fallback.
        """
        # #region agent log
        import json
        import os
        try:
            with open('/Users/hajrezvan/Desktop/Projects/Kebrit/api/.cursor/debug.log', 'a') as f:
                log_entry = json.dumps({
                    "sessionId": "debug-session",
                    "runId": "run1",
                    "hypothesisId": "C",
                    "location": "authentication.py:15",
                    "message": "Checking for JWT token in request",
                    "data": {
                        "has_authorization_header": bool(request.META.get('HTTP_AUTHORIZATION')),
                        "has_token_query_param": bool(request.GET.get('token')),
                        "has_launch_id_query_param": bool(request.GET.get('launch_id')),
                        "has_access_token_cookie": bool(request.COOKIES.get(settings.SIMPLE_JWT.get('AUTH_COOKIE', 'access_token'))),
                        "path": request.path
                    },
                    "timestamp": int(__import__('time').time() * 1000)
                }) + "\n"
                f.write(log_entry)
        except Exception:
            pass
        # #endregion
        
        header = super().get_header(request)
        if header:
            return header

        # Try to get access token from query parameter (for launch-based access)
        access_token = request.GET.get('token')
        if access_token:
            # Format it as Bearer token for parent class processing
            return f"{settings.SIMPLE_JWT['AUTH_HEADER_TYPES'][0]} {access_token}".encode('utf-8')

        # Try to get access token from cookie
        access_token = request.COOKIES.get(settings.SIMPLE_JWT.get('AUTH_COOKIE', 'access_token'))
        if access_token:
            # Format it as Bearer token for parent class processing
            return f"{settings.SIMPLE_JWT['AUTH_HEADER_TYPES'][0]} {access_token}".encode('utf-8')

        return None
    
    def authenticate(self, request):
        """
        Authenticate using JWT token from header or cookie.
        """
        # #region agent log
        import json
        try:
            with open('/Users/hajrezvan/Desktop/Projects/Kebrit/api/.cursor/debug.log', 'a') as f:
                log_entry = json.dumps({
                    "sessionId": "debug-session",
                    "runId": "run1",
                    "hypothesisId": "C",
                    "location": "authentication.py:32",
                    "message": "authenticate method called",
                    "data": {
                        "path": request.path,
                        "method": request.method
                    },
                    "timestamp": int(__import__('time').time() * 1000)
                }) + "\n"
                f.write(log_entry)
        except Exception:
            pass
        # #endregion
        
        header = self.get_header(request)
        if header is None:
            # #region agent log
            try:
                with open('/Users/hajrezvan/Desktop/Projects/Kebrit/api/.cursor/debug.log', 'a') as f:
                    log_entry = json.dumps({
                        "sessionId": "debug-session",
                        "runId": "run1",
                        "hypothesisId": "C",
                        "location": "authentication.py:45",
                        "message": "No header found, returning None",
                        "data": {},
                        "timestamp": int(__import__('time').time() * 1000)
                    }) + "\n"
                    f.write(log_entry)
            except Exception:
                pass
            # #endregion
            return None
        
        raw_token = self.get_raw_token(header)
        if raw_token is None:
            # #region agent log
            try:
                with open('/Users/hajrezvan/Desktop/Projects/Kebrit/api/.cursor/debug.log', 'a') as f:
                    log_entry = json.dumps({
                        "sessionId": "debug-session",
                        "runId": "run1",
                        "hypothesisId": "C",
                        "location": "authentication.py:55",
                        "message": "No raw token extracted, returning None",
                        "data": {},
                        "timestamp": int(__import__('time').time() * 1000)
                    }) + "\n"
                    f.write(log_entry)
            except Exception:
                pass
            # #endregion
            return None
        
        try:
            validated_token = self.get_validated_token(raw_token)
            user = self.get_user(validated_token)
            # #region agent log
            try:
                with open('/Users/hajrezvan/Desktop/Projects/Kebrit/api/.cursor/debug.log', 'a') as f:
                    log_entry = json.dumps({
                        "sessionId": "debug-session",
                        "runId": "run1",
                        "hypothesisId": "C",
                        "location": "authentication.py:70",
                        "message": "Authentication successful",
                        "data": {
                            "user_id": user.id if hasattr(user, 'id') else None,
                            "user_type": type(user).__name__
                        },
                        "timestamp": int(__import__('time').time() * 1000)
                    }) + "\n"
                    f.write(log_entry)
            except Exception:
                pass
            # #endregion
            return (user, validated_token)
        except Exception as e:
            # #region agent log
            try:
                with open('/Users/hajrezvan/Desktop/Projects/Kebrit/api/.cursor/debug.log', 'a') as f:
                    log_entry = json.dumps({
                        "sessionId": "debug-session",
                        "runId": "run1",
                        "hypothesisId": "C",
                        "location": "authentication.py:85",
                        "message": "Authentication failed",
                        "data": {
                            "error": str(e),
                            "error_type": type(e).__name__
                        },
                        "timestamp": int(__import__('time').time() * 1000)
                    }) + "\n"
                    f.write(log_entry)
            except Exception:
                pass
            # #endregion
            return None
    
    def get_user(self, validated_token):
        """
        Attempts to find and return a user using the given validated token.
        Adds custom claims to user object for easy access in permissions.
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
        
        # Add custom claims to user object for easy access in permissions
        user.roles = validated_token.get('roles', [])
        user.is_admin = validated_token.get('is_admin', False)
        user.permissions = validated_token.get('permissions', [])
        user.company_id = validated_token.get('company_id')
        
        return user

