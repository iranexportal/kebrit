from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator
from .models import Level, UserLevel, Badge, UserBadge, UserPoint, UserAction
from .serializers import (
    LevelSerializer, UserLevelSerializer, BadgeSerializer,
    UserBadgeSerializer, UserPointSerializer, UserActionSerializer
)
from users_app.permissions import CompanyPermission


@method_decorator(ratelimit(key='ip', rate='100/h', method='GET'), name='list')
@method_decorator(ratelimit(key='ip', rate='50/h', method='POST'), name='create')
@method_decorator(ratelimit(key='ip', rate='100/h', method='GET'), name='retrieve')
@method_decorator(ratelimit(key='ip', rate='50/h', method='PUT'), name='update')
@method_decorator(ratelimit(key='ip', rate='50/h', method='PATCH'), name='partial_update')
@method_decorator(ratelimit(key='ip', rate='50/h', method='DELETE'), name='destroy')
class LevelViewSet(viewsets.ModelViewSet):
    queryset = Level.objects.select_related('company').all()
    serializer_class = LevelSerializer
    permission_classes = [CompanyPermission]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        if hasattr(self.request, 'auth_company') and self.request.auth_company:
            queryset = queryset.filter(company_id=self.request.auth_company.id)
        queryset = queryset.order_by('order')
        return queryset


@method_decorator(ratelimit(key='ip', rate='100/h', method='GET'), name='list')
@method_decorator(ratelimit(key='ip', rate='50/h', method='POST'), name='create')
@method_decorator(ratelimit(key='ip', rate='100/h', method='GET'), name='retrieve')
@method_decorator(ratelimit(key='ip', rate='50/h', method='PUT'), name='update')
@method_decorator(ratelimit(key='ip', rate='50/h', method='PATCH'), name='partial_update')
@method_decorator(ratelimit(key='ip', rate='50/h', method='DELETE'), name='destroy')
class UserLevelViewSet(viewsets.ModelViewSet):
    queryset = UserLevel.objects.select_related('user', 'user__company', 'level').all()
    serializer_class = UserLevelSerializer
    permission_classes = [CompanyPermission]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        if hasattr(self.request, 'auth_company') and self.request.auth_company:
            queryset = queryset.filter(user__company_id=self.request.auth_company.id)
        queryset = queryset.order_by('-reachedat', '-id')
        return queryset


@method_decorator(ratelimit(key='ip', rate='100/h', method='GET'), name='list')
@method_decorator(ratelimit(key='ip', rate='50/h', method='POST'), name='create')
@method_decorator(ratelimit(key='ip', rate='100/h', method='GET'), name='retrieve')
@method_decorator(ratelimit(key='ip', rate='50/h', method='PUT'), name='update')
@method_decorator(ratelimit(key='ip', rate='50/h', method='PATCH'), name='partial_update')
@method_decorator(ratelimit(key='ip', rate='50/h', method='DELETE'), name='destroy')
class BadgeViewSet(viewsets.ModelViewSet):
    queryset = Badge.objects.select_related('company', 'mission').all()
    serializer_class = BadgeSerializer
    permission_classes = [CompanyPermission]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        if hasattr(self.request, 'auth_company') and self.request.auth_company:
            queryset = queryset.filter(company_id=self.request.auth_company.id)
        queryset = queryset.order_by('id')
        return queryset


@method_decorator(ratelimit(key='ip', rate='100/h', method='GET'), name='list')
@method_decorator(ratelimit(key='ip', rate='50/h', method='POST'), name='create')
@method_decorator(ratelimit(key='ip', rate='100/h', method='GET'), name='retrieve')
@method_decorator(ratelimit(key='ip', rate='50/h', method='PUT'), name='update')
@method_decorator(ratelimit(key='ip', rate='50/h', method='PATCH'), name='partial_update')
@method_decorator(ratelimit(key='ip', rate='50/h', method='DELETE'), name='destroy')
class UserBadgeViewSet(viewsets.ModelViewSet):
    queryset = UserBadge.objects.select_related('user', 'user__company', 'badge').all()
    serializer_class = UserBadgeSerializer
    permission_classes = [CompanyPermission]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        if hasattr(self.request, 'auth_company') and self.request.auth_company:
            queryset = queryset.filter(user__company_id=self.request.auth_company.id)
        queryset = queryset.order_by('-earnedat', '-id')
        return queryset


@method_decorator(ratelimit(key='ip', rate='100/h', method='GET'), name='list')
@method_decorator(ratelimit(key='ip', rate='50/h', method='POST'), name='create')
@method_decorator(ratelimit(key='ip', rate='100/h', method='GET'), name='retrieve')
@method_decorator(ratelimit(key='ip', rate='50/h', method='PUT'), name='update')
@method_decorator(ratelimit(key='ip', rate='50/h', method='PATCH'), name='partial_update')
@method_decorator(ratelimit(key='ip', rate='50/h', method='DELETE'), name='destroy')
class UserPointViewSet(viewsets.ModelViewSet):
    queryset = UserPoint.objects.select_related('user', 'user__company').all()
    serializer_class = UserPointSerializer
    permission_classes = [CompanyPermission]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        if hasattr(self.request, 'auth_company') and self.request.auth_company:
            queryset = queryset.filter(user__company_id=self.request.auth_company.id)
        queryset = queryset.order_by('-totalpoints', '-id')
        return queryset


@method_decorator(ratelimit(key='ip', rate='100/h', method='GET'), name='list')
@method_decorator(ratelimit(key='ip', rate='50/h', method='POST'), name='create')
@method_decorator(ratelimit(key='ip', rate='100/h', method='GET'), name='retrieve')
@method_decorator(ratelimit(key='ip', rate='50/h', method='PUT'), name='update')
@method_decorator(ratelimit(key='ip', rate='50/h', method='PATCH'), name='partial_update')
@method_decorator(ratelimit(key='ip', rate='50/h', method='DELETE'), name='destroy')
class UserActionViewSet(viewsets.ModelViewSet):
    queryset = UserAction.objects.select_related('user', 'user__company').all()
    serializer_class = UserActionSerializer
    permission_classes = [CompanyPermission]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        if hasattr(self.request, 'auth_company') and self.request.auth_company:
            queryset = queryset.filter(user__company_id=self.request.auth_company.id)
        queryset = queryset.order_by('-createdat', '-id')
        return queryset
