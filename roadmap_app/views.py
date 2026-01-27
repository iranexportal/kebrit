from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator
from .models import Mission, MissionRelation, MissionResult, Ability
from .serializers import (
    MissionSerializer, MissionRelationSerializer,
    MissionResultSerializer, AbilitySerializer, UserMissionQuerySerializer
)
from users_app.permissions import CompanyPermission
from users_app.models import User, Company
from kebrit_api.authentication_client import ClientTokenAuthentication
from kebrit_api.permissions import IsClientTokenAuthenticated


@method_decorator(ratelimit(key='ip', rate='100/h', method='GET'), name='list')
@method_decorator(ratelimit(key='ip', rate='50/h', method='POST'), name='create')
@method_decorator(ratelimit(key='ip', rate='100/h', method='GET'), name='retrieve')
@method_decorator(ratelimit(key='ip', rate='50/h', method='PUT'), name='update')
@method_decorator(ratelimit(key='ip', rate='50/h', method='PATCH'), name='partial_update')
@method_decorator(ratelimit(key='ip', rate='50/h', method='DELETE'), name='destroy')
class MissionViewSet(viewsets.ModelViewSet):
    queryset = Mission.objects.select_related('company', 'user').all()
    serializer_class = MissionSerializer
    permission_classes = [CompanyPermission]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        # احراز هویت فقط با Client Token انجام می‌شود
        if hasattr(self.request, 'auth_company') and self.request.auth_company:
            queryset = queryset.filter(company_id=self.request.auth_company.id)
        return queryset
    
    def get_serializer_context(self):
        """اضافه کردن request به context برای دسترسی به کاربر در serializer"""
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


@method_decorator(ratelimit(key='ip', rate='100/h', method='GET'), name='list')
@method_decorator(ratelimit(key='ip', rate='50/h', method='POST'), name='create')
@method_decorator(ratelimit(key='ip', rate='100/h', method='GET'), name='retrieve')
@method_decorator(ratelimit(key='ip', rate='50/h', method='PUT'), name='update')
@method_decorator(ratelimit(key='ip', rate='50/h', method='PATCH'), name='partial_update')
@method_decorator(ratelimit(key='ip', rate='50/h', method='DELETE'), name='destroy')
class MissionRelationViewSet(viewsets.ModelViewSet):
    queryset = MissionRelation.objects.select_related('mission', 'mission__company', 'parent', 'child').all()
    serializer_class = MissionRelationSerializer
    permission_classes = [CompanyPermission]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        if hasattr(self.request, 'auth_company') and self.request.auth_company:
            queryset = queryset.filter(mission__company_id=self.request.auth_company.id)
        return queryset


@method_decorator(ratelimit(key='ip', rate='100/h', method='GET'), name='list')
@method_decorator(ratelimit(key='ip', rate='50/h', method='POST'), name='create')
@method_decorator(ratelimit(key='ip', rate='100/h', method='GET'), name='retrieve')
@method_decorator(ratelimit(key='ip', rate='50/h', method='PUT'), name='update')
@method_decorator(ratelimit(key='ip', rate='50/h', method='PATCH'), name='partial_update')
@method_decorator(ratelimit(key='ip', rate='50/h', method='DELETE'), name='destroy')
class MissionResultViewSet(viewsets.ModelViewSet):
    queryset = MissionResult.objects.select_related('mission', 'mission__company', 'user', 'user__company', 'ability').all()
    serializer_class = MissionResultSerializer
    permission_classes = [CompanyPermission]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        if hasattr(self.request, 'auth_company') and self.request.auth_company:
            queryset = queryset.filter(user__company_id=self.request.auth_company.id)
        return queryset


@method_decorator(ratelimit(key='ip', rate='100/h', method='GET'), name='list')
@method_decorator(ratelimit(key='ip', rate='50/h', method='POST'), name='create')
@method_decorator(ratelimit(key='ip', rate='100/h', method='GET'), name='retrieve')
@method_decorator(ratelimit(key='ip', rate='50/h', method='PUT'), name='update')
@method_decorator(ratelimit(key='ip', rate='50/h', method='PATCH'), name='partial_update')
@method_decorator(ratelimit(key='ip', rate='50/h', method='DELETE'), name='destroy')
class AbilityViewSet(viewsets.ModelViewSet):
    queryset = Ability.objects.select_related('company').all()
    serializer_class = AbilitySerializer
    permission_classes = [CompanyPermission]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        if hasattr(self.request, 'auth_company') and self.request.auth_company:
            queryset = queryset.filter(company_id=self.request.auth_company.id)
        return queryset


@api_view(['POST'])
@authentication_classes([ClientTokenAuthentication])
@permission_classes([IsClientTokenAuthenticated])
@ratelimit(key='ip', rate='100/h', method='POST')
def get_user_missions(request):
    """
    دریافت ماموریت‌های انجام شده و در دسترس کاربر
    
    این endpoint با دریافت شماره تلفن و شناسه شرکت، ماموریت‌های انجام شده
    و در دسترس کاربر را برمی‌گرداند.
    
    Body:
    {
        "mobile": "09123456789",
        "company_id": 1
    }
    
    Response:
    {
        "user": {
            "id": 1,
            "name": "نام کاربر",
            "mobile": "09123456789"
        },
        "completed_missions": [...],
        "available_missions": [...]
    }
    """
    serializer = UserMissionQuerySerializer(data=request.data)
    if not serializer.is_valid():
        return Response(
            {'error': serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    mobile = serializer.validated_data['mobile']
    
    # شرکت از روی توکن مشتری (ClientTokenAuthentication) تعیین می‌شود
    company = getattr(request, 'auth_company', None)
    if company is None:
        return Response(
            {'error': 'توکن مشتری نامعتبر است'},
            status=status.HTTP_401_UNAUTHORIZED
        )
    company_id = company.id
    
    # بررسی وجود کاربر با شماره تلفن و شرکت
    try:
        user = User.objects.select_related('company').get(mobile=mobile, company_id=company_id)
    except User.DoesNotExist:
        return Response(
            {'error': 'کاربر با این شماره تلفن در این شرکت یافت نشد'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    # دریافت ماموریت‌های انجام شده کاربر (فیلتر شده بر اساس company_id)
    completed_results = MissionResult.objects.filter(
        user=user,
        mission__company_id=company_id
    ).select_related('mission', 'mission__company', 'ability')
    
    completed_missions_data = []
    completed_mission_ids = []
    
    for result in completed_results:
        completed_mission_ids.append(result.mission_id)
        mission_serializer = MissionSerializer(result.mission, context={'request': request})
        result_serializer = MissionResultSerializer(result, context={'request': request})
        completed_missions_data.append({
            'mission': mission_serializer.data,
            'result': result_serializer.data
        })
    
    # دریافت ماموریت‌های در دسترس (فیلتر شده بر اساس company_id و حذف ماموریت‌های انجام شده)
    available_missions = Mission.objects.filter(
        company_id=company_id,
        is_active=True
    ).exclude(
        id__in=completed_mission_ids
    ).select_related('company', 'user')
    
    available_missions_serializer = MissionSerializer(available_missions, many=True, context={'request': request})
    
    return Response({
        'user': {
            'id': user.id,
            'name': user.name,
            'mobile': user.mobile,
            'company_id': user.company_id,
            'company_name': user.company.name
        },
        'completed_missions': completed_missions_data,
        'available_missions': available_missions_serializer.data,
        'stats': {
            'total_completed': len(completed_missions_data),
            'total_available': available_missions.count()
        }
    }, status=status.HTTP_200_OK)
