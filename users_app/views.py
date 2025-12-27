from rest_framework import viewsets
from rest_framework.decorators import action
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator
from .models import Company, User, Session, Token, Role, UserRole
from .serializers import (
    CompanySerializer, UserSerializer, SessionSerializer,
    TokenSerializer, RoleSerializer, UserRoleSerializer
)
from .permissions import CompanyPermission, IsAdminOrReadOnly


@method_decorator(ratelimit(key='ip', rate='100/h', method='GET'), name='list')
@method_decorator(ratelimit(key='ip', rate='50/h', method='POST'), name='create')
@method_decorator(ratelimit(key='ip', rate='100/h', method='GET'), name='retrieve')
@method_decorator(ratelimit(key='ip', rate='50/h', method='PUT'), name='update')
@method_decorator(ratelimit(key='ip', rate='50/h', method='PATCH'), name='partial_update')
@method_decorator(ratelimit(key='ip', rate='50/h', method='DELETE'), name='destroy')
class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [CompanyPermission, IsAdminOrReadOnly]


@method_decorator(ratelimit(key='ip', rate='100/h', method='GET'), name='list')
@method_decorator(ratelimit(key='ip', rate='50/h', method='POST'), name='create')
@method_decorator(ratelimit(key='ip', rate='100/h', method='GET'), name='retrieve')
@method_decorator(ratelimit(key='ip', rate='50/h', method='PUT'), name='update')
@method_decorator(ratelimit(key='ip', rate='50/h', method='PATCH'), name='partial_update')
@method_decorator(ratelimit(key='ip', rate='50/h', method='DELETE'), name='destroy')
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.select_related('company').all()
    serializer_class = UserSerializer
    permission_classes = [CompanyPermission]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        # Filter by companyId for non-admin users
        if hasattr(self.request.user, 'company_id'):
            user_roles = self.request.user.user_roles.all()
            is_admin = any(ur.role.title.lower() == 'admin' for ur in user_roles)
            if not is_admin:
                queryset = queryset.filter(company_id=self.request.user.company_id)
        return queryset


@method_decorator(ratelimit(key='ip', rate='100/h', method='GET'), name='list')
@method_decorator(ratelimit(key='ip', rate='50/h', method='POST'), name='create')
@method_decorator(ratelimit(key='ip', rate='100/h', method='GET'), name='retrieve')
@method_decorator(ratelimit(key='ip', rate='50/h', method='PUT'), name='update')
@method_decorator(ratelimit(key='ip', rate='50/h', method='PATCH'), name='partial_update')
@method_decorator(ratelimit(key='ip', rate='50/h', method='DELETE'), name='destroy')
class SessionViewSet(viewsets.ModelViewSet):
    queryset = Session.objects.select_related('user', 'user__company').all()
    serializer_class = SessionSerializer
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
class TokenViewSet(viewsets.ModelViewSet):
    queryset = Token.objects.select_related('user', 'user__company').all()
    serializer_class = TokenSerializer
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
class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.select_related('company').all()
    serializer_class = RoleSerializer
    permission_classes = [CompanyPermission]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        if hasattr(self.request.user, 'company_id'):
            user_roles = self.request.user.user_roles.all()
            is_admin = any(ur.role.title.lower() == 'admin' for ur in user_roles)
            if not is_admin:
                queryset = queryset.filter(company_id=self.request.user.company_id)
        return queryset


@method_decorator(ratelimit(key='ip', rate='100/h', method='GET'), name='list')
@method_decorator(ratelimit(key='ip', rate='50/h', method='POST'), name='create')
@method_decorator(ratelimit(key='ip', rate='100/h', method='GET'), name='retrieve')
@method_decorator(ratelimit(key='ip', rate='50/h', method='PUT'), name='update')
@method_decorator(ratelimit(key='ip', rate='50/h', method='PATCH'), name='partial_update')
@method_decorator(ratelimit(key='ip', rate='50/h', method='DELETE'), name='destroy')
class UserRoleViewSet(viewsets.ModelViewSet):
    queryset = UserRole.objects.select_related('user', 'user__company', 'role').all()
    serializer_class = UserRoleSerializer
    permission_classes = [CompanyPermission]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        if hasattr(self.request.user, 'company_id'):
            user_roles = self.request.user.user_roles.all()
            is_admin = any(ur.role.title.lower() == 'admin' for ur in user_roles)
            if not is_admin:
                queryset = queryset.filter(user__company_id=self.request.user.company_id)
        return queryset
