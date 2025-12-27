from rest_framework import viewsets
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator
from .models import Evaluation, Question, Quiz, QuizResponse, QuizResponseEvaluation
from .serializers import (
    EvaluationSerializer, QuestionSerializer, QuizSerializer,
    QuizResponseSerializer, QuizResponseEvaluationSerializer
)
from users_app.permissions import CompanyPermission


@method_decorator(ratelimit(key='ip', rate='100/h', method='GET'), name='list')
@method_decorator(ratelimit(key='ip', rate='50/h', method='POST'), name='create')
@method_decorator(ratelimit(key='ip', rate='100/h', method='GET'), name='retrieve')
@method_decorator(ratelimit(key='ip', rate='50/h', method='PUT'), name='update')
@method_decorator(ratelimit(key='ip', rate='50/h', method='PATCH'), name='partial_update')
@method_decorator(ratelimit(key='ip', rate='50/h', method='DELETE'), name='destroy')
class EvaluationViewSet(viewsets.ModelViewSet):
    queryset = Evaluation.objects.select_related('mission', 'mission__company', 'user', 'user__company').all()
    serializer_class = EvaluationSerializer
    permission_classes = [CompanyPermission]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        if hasattr(self.request.user, 'company_id'):
            user_roles = self.request.user.user_roles.all()
            is_admin = any(ur.role.title.lower() == 'admin' for ur in user_roles)
            if not is_admin:
                queryset = queryset.filter(user__company_id=self.request.user.company_id)
        return queryset


@method_decorator(ratelimit(key='ip', rate='100/h', method='GET'), name='list')
@method_decorator(ratelimit(key='ip', rate='50/h', method='POST'), name='create')
@method_decorator(ratelimit(key='ip', rate='100/h', method='GET'), name='retrieve')
@method_decorator(ratelimit(key='ip', rate='50/h', method='PUT'), name='update')
@method_decorator(ratelimit(key='ip', rate='50/h', method='PATCH'), name='partial_update')
@method_decorator(ratelimit(key='ip', rate='50/h', method='DELETE'), name='destroy')
class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.select_related('evaluation', 'evaluation__user', 'evaluation__user__company').all()
    serializer_class = QuestionSerializer
    permission_classes = [CompanyPermission]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        if hasattr(self.request.user, 'company_id'):
            user_roles = self.request.user.user_roles.all()
            is_admin = any(ur.role.title.lower() == 'admin' for ur in user_roles)
            if not is_admin:
                queryset = queryset.filter(evaluation__user__company_id=self.request.user.company_id)
        return queryset


@method_decorator(ratelimit(key='ip', rate='100/h', method='GET'), name='list')
@method_decorator(ratelimit(key='ip', rate='50/h', method='POST'), name='create')
@method_decorator(ratelimit(key='ip', rate='100/h', method='GET'), name='retrieve')
@method_decorator(ratelimit(key='ip', rate='50/h', method='PUT'), name='update')
@method_decorator(ratelimit(key='ip', rate='50/h', method='PATCH'), name='partial_update')
@method_decorator(ratelimit(key='ip', rate='50/h', method='DELETE'), name='destroy')
class QuizViewSet(viewsets.ModelViewSet):
    queryset = Quiz.objects.select_related('evaluation', 'evaluation__user', 'evaluation__user__company', 'user', 'user__company').all()
    serializer_class = QuizSerializer
    permission_classes = [CompanyPermission]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        if hasattr(self.request.user, 'company_id'):
            user_roles = self.request.user.user_roles.all()
            is_admin = any(ur.role.title.lower() == 'admin' for ur in user_roles)
            if not is_admin:
                queryset = queryset.filter(user__company_id=self.request.user.company_id)
        return queryset


@method_decorator(ratelimit(key='ip', rate='100/h', method='GET'), name='list')
@method_decorator(ratelimit(key='ip', rate='50/h', method='POST'), name='create')
@method_decorator(ratelimit(key='ip', rate='100/h', method='GET'), name='retrieve')
@method_decorator(ratelimit(key='ip', rate='50/h', method='PUT'), name='update')
@method_decorator(ratelimit(key='ip', rate='50/h', method='PATCH'), name='partial_update')
@method_decorator(ratelimit(key='ip', rate='50/h', method='DELETE'), name='destroy')
class QuizResponseViewSet(viewsets.ModelViewSet):
    queryset = QuizResponse.objects.select_related('quiz', 'quiz__user', 'quiz__user__company', 'question').all()
    serializer_class = QuizResponseSerializer
    permission_classes = [CompanyPermission]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        if hasattr(self.request.user, 'company_id'):
            user_roles = self.request.user.user_roles.all()
            is_admin = any(ur.role.title.lower() == 'admin' for ur in user_roles)
            if not is_admin:
                queryset = queryset.filter(quiz__user__company_id=self.request.user.company_id)
        return queryset


@method_decorator(ratelimit(key='ip', rate='100/h', method='GET'), name='list')
@method_decorator(ratelimit(key='ip', rate='50/h', method='POST'), name='create')
@method_decorator(ratelimit(key='ip', rate='100/h', method='GET'), name='retrieve')
@method_decorator(ratelimit(key='ip', rate='50/h', method='PUT'), name='update')
@method_decorator(ratelimit(key='ip', rate='50/h', method='PATCH'), name='partial_update')
@method_decorator(ratelimit(key='ip', rate='50/h', method='DELETE'), name='destroy')
class QuizResponseEvaluationViewSet(viewsets.ModelViewSet):
    queryset = QuizResponseEvaluation.objects.select_related('user', 'user__company', 'quiz_response', 'quiz_response__quiz', 'quiz_response__quiz__user').all()
    serializer_class = QuizResponseEvaluationSerializer
    permission_classes = [CompanyPermission]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        if hasattr(self.request.user, 'company_id'):
            user_roles = self.request.user.user_roles.all()
            is_admin = any(ur.role.title.lower() == 'admin' for ur in user_roles)
            if not is_admin:
                queryset = queryset.filter(user__company_id=self.request.user.company_id)
        return queryset
