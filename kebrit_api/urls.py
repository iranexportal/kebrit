"""
URL configuration for kebrit_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

# Import all viewsets
from users_app.views import (
    CompanyViewSet, UserViewSet, SessionViewSet,
    TokenViewSet, RoleViewSet, UserRoleViewSet
)
from roadmap_app.views import (
    MissionViewSet, MissionRelationViewSet,
    MissionResultViewSet, AbilityViewSet
)
from exam_app.views import (
    EvaluationViewSet, QuestionViewSet, QuizViewSet,
    QuizResponseViewSet, QuizResponseEvaluationViewSet
)
from media_app.views import (
    FileViewSet, TagViewSet, FileTagViewSet
)

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
router.register(r'evaluations', EvaluationViewSet, basename='evaluation')
router.register(r'questions', QuestionViewSet, basename='question')
router.register(r'quizzes', QuizViewSet, basename='quiz')
router.register(r'quiz-responses', QuizResponseViewSet, basename='quizresponse')
router.register(r'quiz-response-evaluations', QuizResponseEvaluationViewSet, basename='quizresponseevaluation')

# Media app routes
router.register(r'files', FileViewSet, basename='file')
router.register(r'tags', TagViewSet, basename='tag')
router.register(r'file-tags', FileTagViewSet, basename='filetag')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    # JWT Authentication endpoints
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
