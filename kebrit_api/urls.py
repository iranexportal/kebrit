"""
URL configuration for kebrit_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from users_app.serializers import CustomTokenObtainPairSerializer


# ADD THIS: Custom token obtain view that sets cookies
class CookieTokenObtainPairView(TokenObtainPairView):
    """
    Token obtain view that sets HttpOnly cookies in addition to returning tokens in response.
    Maintains backward compatibility with header-based authentication.
    """
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        
        if response.status_code == 200:
            # Set cookies from response data
            access_token = response.data.get('access')
            refresh_token = response.data.get('refresh')
            
            if access_token:
                response.set_cookie(
                    'access_token',
                    access_token,
                    max_age=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds(),
                    httponly=True,
                    secure=not settings.DEBUG,
                    samesite='Lax',
                    path='/'
                )
            
            if refresh_token:
                response.set_cookie(
                    'refresh_token',
                    refresh_token,
                    max_age=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'].total_seconds(),
                    httponly=True,
                    secure=not settings.DEBUG,
                    samesite='Lax',
                    path='/'
                )
        
        return response


# ADD THIS: Custom token refresh view that supports cookies
class CookieTokenRefreshView(TokenRefreshView):
    """
    Token refresh view that supports both cookie and header-based tokens.
    """
    def post(self, request, *args, **kwargs):
        # Try to get refresh token from cookie first
        refresh_token = request.COOKIES.get(settings.SIMPLE_JWT.get('AUTH_COOKIE_REFRESH', 'refresh_token'))
        
        # Fallback to request body
        if not refresh_token:
            refresh_token = request.data.get('refresh')
        
        if not refresh_token:
            return Response(
                {'error': 'Refresh token not provided'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Validate and refresh token
        try:
            from rest_framework_simplejwt.tokens import RefreshToken
            refresh = RefreshToken(refresh_token)
            access_token = refresh.access_token
            
            response = Response({
                'access': str(access_token)
            }, status=status.HTTP_200_OK)
            
            # Set new access token in cookie
            response.set_cookie(
                'access_token',
                str(access_token),
                max_age=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds(),
                httponly=True,
                secure=not settings.DEBUG,
                samesite='Lax',
                path='/'
            )
            
            return response
        except (InvalidToken, TokenError) as e:
            return Response(
                {'error': 'Invalid refresh token'},
                status=status.HTTP_401_UNAUTHORIZED
            )


# ADD THIS: Token logout view to clear cookies
class TokenLogoutView(TokenRefreshView):
    """
    Logout view that clears JWT cookies and blacklists refresh token.
    """
    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get(settings.SIMPLE_JWT.get('AUTH_COOKIE_REFRESH', 'refresh_token'))
        
        if not refresh_token:
            refresh_token = request.data.get('refresh')
        
        # Blacklist the refresh token if provided
        if refresh_token:
            try:
                from rest_framework_simplejwt.tokens import RefreshToken
                from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
                
                token = RefreshToken(refresh_token)
                token.blacklist()
            except Exception:
                pass  # Ignore errors during logout
        
        response = Response(
            {'message': 'Successfully logged out'},
            status=status.HTTP_200_OK
        )
        
        # Clear cookies
        response.delete_cookie('access_token', path='/')
        response.delete_cookie('refresh_token', path='/')
        
        return response

# Import all viewsets
from users_app.views import (
    CompanyViewSet, UserViewSet, SessionViewSet,
    TokenViewSet, RoleViewSet, UserRoleViewSet, login
)
from roadmap_app.views import (
    MissionViewSet, MissionRelationViewSet,
    MissionResultViewSet, AbilityViewSet, get_user_missions
)
from exam_app.views import (
    EvaluationTypeViewSet, EvaluationViewSet, QuestionViewSet, QuizViewSet,
    QuizResponseViewSet, QuizResponseEvaluationViewSet
)
from media_app.views import (
    FileViewSet, TagViewSet, FileTagViewSet
)
from gaming_app.views import (
    LevelViewSet, UserLevelViewSet, BadgeViewSet,
    UserBadgeViewSet, UserPointViewSet, UserActionViewSet
)


# ADD THIS: Custom token refresh view that supports cookies
class CookieTokenRefreshView(TokenRefreshView):
    """
    Token refresh view that supports both cookie and header-based tokens.
    """
    def post(self, request, *args, **kwargs):
        # Try to get refresh token from cookie first
        refresh_token = request.COOKIES.get(settings.SIMPLE_JWT.get('AUTH_COOKIE_REFRESH', 'refresh_token'))
        
        # Fallback to request body
        if not refresh_token:
            refresh_token = request.data.get('refresh')
        
        if not refresh_token:
            return Response(
                {'error': 'Refresh token not provided'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Validate and refresh token
        try:
            from rest_framework_simplejwt.tokens import RefreshToken
            refresh = RefreshToken(refresh_token)
            access_token = refresh.access_token
            
            response = Response({
                'access': str(access_token)
            }, status=status.HTTP_200_OK)
            
            # Set new access token in cookie
            response.set_cookie(
                'access_token',
                str(access_token),
                max_age=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds(),
                httponly=True,
                secure=not settings.DEBUG,
                samesite='Lax',
                path='/'
            )
            
            return response
        except (InvalidToken, TokenError) as e:
            return Response(
                {'error': 'Invalid refresh token'},
                status=status.HTTP_401_UNAUTHORIZED
            )


# ADD THIS: Token logout view to clear cookies
class TokenLogoutView(TokenRefreshView):
    """
    Logout view that clears JWT cookies and blacklists refresh token.
    """
    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get(settings.SIMPLE_JWT.get('AUTH_COOKIE_REFRESH', 'refresh_token'))
        
        if not refresh_token:
            refresh_token = request.data.get('refresh')
        
        # Blacklist the refresh token if provided
        if refresh_token:
            try:
                from rest_framework_simplejwt.tokens import RefreshToken
                from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
                
                token = RefreshToken(refresh_token)
                token.blacklist()
            except Exception:
                pass  # Ignore errors during logout
        
        response = Response(
            {'message': 'Successfully logged out'},
            status=status.HTTP_200_OK
        )
        
        # Clear cookies
        response.delete_cookie('access_token', path='/')
        response.delete_cookie('refresh_token', path='/')
        
        return response


# Create routers for each app
router = routers.DefaultRouter()

# Users app routes
router.register(r'companies', CompanyViewSet, basename='company')
router.register(r'users', UserViewSet, basename='user')
router.register(r'sessions', SessionViewSet, basename='session')
router.register(r'tokens', TokenViewSet, basename='token')
router.register(r'roles', RoleViewSet, basename='role')
router.register(r'user-roles', UserRoleViewSet, basename='userrole')

# Roadmap app routes
router.register(r'missions', MissionViewSet, basename='mission')
router.register(r'mission-relations', MissionRelationViewSet, basename='missionrelation')
router.register(r'mission-results', MissionResultViewSet, basename='missionresult')
router.register(r'abilities', AbilityViewSet, basename='ability')

# Exam app routes
router.register(r'evaluation-types', EvaluationTypeViewSet, basename='evaluationtype')
router.register(r'evaluations', EvaluationViewSet, basename='evaluation')
router.register(r'questions', QuestionViewSet, basename='question')
router.register(r'quizzes', QuizViewSet, basename='quiz')
router.register(r'quiz-responses', QuizResponseViewSet, basename='quizresponse')
router.register(r'quiz-response-evaluations', QuizResponseEvaluationViewSet, basename='quizresponseevaluation')

# Media app routes
router.register(r'files', FileViewSet, basename='file')
router.register(r'tags', TagViewSet, basename='tag')
router.register(r'file-tags', FileTagViewSet, basename='filetag')

# Gaming app routes
router.register(r'levels', LevelViewSet, basename='level')
router.register(r'user-levels', UserLevelViewSet, basename='userlevel')
router.register(r'badges', BadgeViewSet, basename='badge')
router.register(r'user-badges', UserBadgeViewSet, basename='userbadge')
router.register(r'user-points', UserPointViewSet, basename='userpoint')
router.register(r'user-actions', UserActionViewSet, basename='useraction')

# Note: csrf_exempt cannot be used directly with include().
# For DRF routers, CSRF exemption is typically handled at the viewset level or via settings.
# REST Framework viewsets handle CSRF exemption automatically for API requests.

urlpatterns = [
    path('admin/', admin.site.urls),  # Admin panel requires CSRF
    # API endpoints are exempt from CSRF (API-only, using JWT)
    path('api/', include(router.urls)),
    # Custom login endpoint with mobile and token (passwordless)
    path('api/login/', csrf_exempt(login), name='login'),
    # Roadmap app custom endpoints
    path('api/user-missions/', csrf_exempt(get_user_missions), name='user_missions'),
    # JWT Authentication endpoints (exempt from CSRF)
    # Custom token view that accepts mobile instead of username and sets cookies
    path('api/token/', csrf_exempt(CookieTokenObtainPairView.as_view(serializer_class=CustomTokenObtainPairSerializer)), name='token_obtain_pair'),
    path('api/token/refresh/', csrf_exempt(CookieTokenRefreshView.as_view()), name='token_refresh'),
    path('api/token/verify/', csrf_exempt(TokenVerifyView.as_view()), name='token_verify'),
    path('api/token/logout/', csrf_exempt(TokenLogoutView.as_view()), name='token_logout'),
]
