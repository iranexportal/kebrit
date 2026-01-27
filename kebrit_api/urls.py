"""
URL configuration for kebrit_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.decorators.csrf import csrf_exempt
from rest_framework import routers
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions




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
from exam_app.integration_views import (
    ClientExamInfoView,
    ClientExamLaunchView,
    LaunchDetailView,
    LaunchAnswerView,
    LaunchSubmitView,
    LaunchRedirectView,
)
from exam_app.views import mission_student_report





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

# Swagger/OpenAPI Schema View
schema_view = get_schema_view(
    openapi.Info(
        title="Kebrit API",
        default_version='v1',
        description="""
        مستندات کامل API سامانه Kebrit
        
        این API برای مدیریت کاربران، آزمون‌ها، ماموریت‌ها، فایل‌ها و سیستم gamification طراحی شده است.
        
        ## احراز هویت
        
        ### برای مشتریان (Integration):
        - استفاده از Client Token
        - Header: `X-Client-Token: <client_token_uuid>`
        - یا: `Authorization: Token <client_token_uuid>`
        
        ## نکات مهم:
        - تمام endpoint های API نیاز به احراز هویت دارند (به جز endpoint های login و launch)
        - برای یکپارچه‌سازی با سامانه Kebrit، به مستندات `docs/INTEGRATION_API.md` مراجعه کنید
        """,
        terms_of_service="https://www.ayareto.com/terms/",
        contact=openapi.Contact(email="support@ayareto.com"),
        license=openapi.License(name="Proprietary"),
    ),
    public=True,  # Allow access without authentication for documentation
    permission_classes=(permissions.AllowAny,),  # Read-only access
    # patterns will be auto-discovered from urlpatterns
)

urlpatterns = [
    path('admin/', admin.site.urls),  # Admin panel requires CSRF
    # API endpoints are exempt from CSRF (API-only, using JWT)
    path('api/', include(router.urls)),
    # Custom login endpoint with mobile and token (passwordless)
    path('api/login/', csrf_exempt(login), name='login'),
    # Customer integration endpoints (client token in header)
    path('api/integration/exams/<int:eurl>/', csrf_exempt(ClientExamInfoView.as_view()), name='integration_exam_info'),
    path('api/integration/exams/launch/', csrf_exempt(ClientExamLaunchView.as_view()), name='integration_exam_launch'),
    # Student quiz endpoints (quiz_id in URL)
    path('api/quiz/<int:quiz_id>/', csrf_exempt(LaunchDetailView.as_view()), name='quiz_detail'),
    path('api/quiz/<int:quiz_id>/answer/', csrf_exempt(LaunchAnswerView.as_view()), name='quiz_answer'),
    path('api/quiz/<int:quiz_id>/submit/', csrf_exempt(LaunchSubmitView.as_view()), name='quiz_submit'),
    path('api/quiz/<int:quiz_id>/redirect/', csrf_exempt(LaunchRedirectView.as_view()), name='quiz_redirect'),
    # Roadmap app custom endpoints
    path('api/user-missions/', csrf_exempt(get_user_missions), name='user_missions'),
    # Mission student report
    path('api/mission-student-report/', csrf_exempt(mission_student_report), name='mission_student_report'),
    # Swagger/OpenAPI Documentation (Read-only - نمایش مستندات بدون امکان اجرا)
    re_path(r'^doc(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('doc/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
