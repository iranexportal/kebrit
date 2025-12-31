from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator
import secrets
import string
from .models import Company, User, Session, Token, Role, UserRole
from .serializers import (
    CompanySerializer, UserSerializer, SessionSerializer,
    TokenSerializer, RoleSerializer, UserRoleSerializer,
    UserCreateSerializer, UserLoginSerializer
)
from .permissions import CompanyPermission, IsAdminOrReadOnly
from rest_framework_simplejwt.tokens import RefreshToken


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
    
    @action(detail=False, methods=['post'], url_path='create', permission_classes=[AllowAny])
    @method_decorator(ratelimit(key='ip', rate='20/h', method='POST'))
    def create_user(self, request):
        """
        ایجاد کاربر جدید با رمز عبور تصادفی
        
        این endpoint یک کاربر جدید می‌سازد و یک رمز عبور 12 کاراکتری تصادفی
        برای او ایجاد می‌کند.
        
        Body:
        {
            "name": "نام کاربر",
            "company_id": 1,
            "uuid": "شناسه یکتای درون سازمانی",
            "mobile": "09123456789"
        }
        """
        serializer = UserCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {'error': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # تولید رمز عبور 12 کاراکتری تصادفی
        # شامل اعداد، حروف بزرگ و کوچک، و کاراکترهای خاص
        alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
        password = ''.join(secrets.choice(alphabet) for _ in range(12))
        
        try:
            company = Company.objects.get(id=serializer.validated_data['company_id'])
            
            # بررسی اینکه uuid در این شرکت تکراری نباشد
            if User.objects.filter(company=company, uuid=serializer.validated_data['uuid']).exists():
                return Response(
                    {'error': 'این شناسه یکتا در این شرکت قبلاً ثبت شده است'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # ایجاد کاربر
            user = User.objects.create(
                name=serializer.validated_data['name'],
                company=company,
                uuid=serializer.validated_data['uuid'],
                mobile=serializer.validated_data['mobile'],
                password=password
            )
            
            return Response({
                'message': 'کاربر با موفقیت ایجاد شد',
                'user_id': user.id,
                'name': user.name,
                'mobile': user.mobile,
                'company': company.name,
                'password': password  # فقط یک بار نمایش داده می‌شود
            }, status=status.HTTP_201_CREATED)
            
        except Company.DoesNotExist:
            return Response(
                {'error': 'شرکت یافت نشد'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': f'خطا در ایجاد کاربر: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['get'], url_path='company/(?P<company_id>[^/.]+)')
    @method_decorator(ratelimit(key='ip', rate='100/h', method='GET'))
    def list_by_company(self, request, company_id=None):
        """
        لیست تمام کاربران یک سازمان
        
        این endpoint تمام کاربرانی که در سامانه لاگین کرده‌اند و
        متعلق به یک سازمان خاص هستند را برمی‌گرداند.
        """
        try:
            company = Company.objects.get(id=company_id)
        except Company.DoesNotExist:
            return Response(
                {'error': 'سازمان یافت نشد'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # بررسی دسترسی
        if hasattr(request.user, 'company_id'):
            user_roles = request.user.user_roles.all()
            is_admin = any(ur.role.title.lower() == 'admin' for ur in user_roles)
            if not is_admin and request.user.company_id != int(company_id):
                return Response(
                    {'error': 'دسترسی به این سازمان ندارید'},
                    status=status.HTTP_403_FORBIDDEN
                )
        
        users = User.objects.filter(company=company).select_related('company')
        serializer = UserSerializer(users, many=True)
        
        return Response({
            'company_id': company.id,
            'company_name': company.name,
            'total_users': users.count(),
            'users': serializer.data
        }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
@ratelimit(key='ip', rate='10/h', method='POST')
def login(request):
    """
    لاگین کاربر با شماره تلفن و رمز عبور
    
    این endpoint کاربر را با شماره تلفن و رمز عبور احراز هویت می‌کند
    و یک JWT token برمی‌گرداند.
    
    Body:
    {
        "mobile": "09123456789",
        "password": "رمزعبور"
    }
    """
    serializer = UserLoginSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(
            {'error': serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    mobile = serializer.validated_data['mobile']
    password = serializer.validated_data['password']
    
    try:
        user = User.objects.get(mobile=mobile)
    except User.DoesNotExist:
        return Response(
            {'error': 'شماره تلفن یا رمز عبور اشتباه است'},
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    # بررسی رمز عبور
    if user.password != password:
        return Response(
            {'error': 'شماره تلفن یا رمز عبور اشتباه است'},
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    # ایجاد JWT token
    refresh = RefreshToken()
    refresh['user_id'] = user.id
    
    # Add role and permissions to token
    user_roles = user.user_roles.select_related('role').all()
    roles = [ur.role.title for ur in user_roles]
    refresh['role'] = roles[0] if roles else None
    refresh['roles'] = roles
    
    # Add permissions based on roles
    permissions = []
    for user_role in user_roles:
        role_title = user_role.role.title.lower()
        if role_title == 'admin':
            permissions.extend(['admin.read', 'admin.write', 'admin.delete'])
    refresh['permissions'] = list(set(permissions))
    
    response = Response({
        'access': str(refresh.access_token),
        'refresh': str(refresh),
        'user': {
            'id': user.id,
            'name': user.name,
            'mobile': user.mobile,
            'company_id': user.company_id,
            'company_name': user.company.name,
            'roles': roles,
            'permissions': refresh['permissions']
        }
    }, status=status.HTTP_200_OK)
    
    # ADD THIS: Set HttpOnly cookies for tokens (keep header response for backward compatibility)
    from django.conf import settings
    response.set_cookie(
        'access_token',
        str(refresh.access_token),
        max_age=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds(),
        httponly=True,
        secure=not settings.DEBUG,
        samesite='Lax',
        path='/'
    )
    response.set_cookie(
        'refresh_token',
        str(refresh),
        max_age=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'].total_seconds(),
        httponly=True,
        secure=not settings.DEBUG,
        samesite='Lax',
        path='/'
    )
    
    return response


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
