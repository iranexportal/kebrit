from rest_framework import viewsets
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator
from .models import File, Tag, FileTag
from .serializers import FileSerializer, TagSerializer, FileTagSerializer
from users_app.permissions import CompanyPermission


@method_decorator(ratelimit(key='ip', rate='100/h', method='GET'), name='list')
@method_decorator(ratelimit(key='ip', rate='50/h', method='POST'), name='create')
@method_decorator(ratelimit(key='ip', rate='100/h', method='GET'), name='retrieve')
@method_decorator(ratelimit(key='ip', rate='50/h', method='PUT'), name='update')
@method_decorator(ratelimit(key='ip', rate='50/h', method='PATCH'), name='partial_update')
@method_decorator(ratelimit(key='ip', rate='50/h', method='DELETE'), name='destroy')
class FileViewSet(viewsets.ModelViewSet):
    queryset = File.objects.select_related('company', 'user', 'user__company').all()
    serializer_class = FileSerializer
    permission_classes = [CompanyPermission]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        if hasattr(self.request, 'auth_company') and self.request.auth_company:
            queryset = queryset.filter(company_id=self.request.auth_company.id)
        return queryset


@method_decorator(ratelimit(key='ip', rate='100/h', method='GET'), name='list')
@method_decorator(ratelimit(key='ip', rate='50/h', method='POST'), name='create')
@method_decorator(ratelimit(key='ip', rate='100/h', method='GET'), name='retrieve')
@method_decorator(ratelimit(key='ip', rate='50/h', method='PUT'), name='update')
@method_decorator(ratelimit(key='ip', rate='50/h', method='PATCH'), name='partial_update')
@method_decorator(ratelimit(key='ip', rate='50/h', method='DELETE'), name='destroy')
class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [CompanyPermission]


@method_decorator(ratelimit(key='ip', rate='100/h', method='GET'), name='list')
@method_decorator(ratelimit(key='ip', rate='50/h', method='POST'), name='create')
@method_decorator(ratelimit(key='ip', rate='100/h', method='GET'), name='retrieve')
@method_decorator(ratelimit(key='ip', rate='50/h', method='PUT'), name='update')
@method_decorator(ratelimit(key='ip', rate='50/h', method='PATCH'), name='partial_update')
@method_decorator(ratelimit(key='ip', rate='50/h', method='DELETE'), name='destroy')
class FileTagViewSet(viewsets.ModelViewSet):
    queryset = FileTag.objects.select_related('file', 'file__company', 'tag').all()
    serializer_class = FileTagSerializer
    permission_classes = [CompanyPermission]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        if hasattr(self.request, 'auth_company') and self.request.auth_company:
            queryset = queryset.filter(file__company_id=self.request.auth_company.id)
        return queryset
