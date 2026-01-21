from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Company, User, Session, Token, Role, UserRole


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class UserCreateSerializer(serializers.Serializer):
    """Serializer for creating a new user (passwordless)."""
    name = serializers.CharField(max_length=100, required=True)
    company_id = serializers.IntegerField(required=True)
    uuid = serializers.CharField(max_length=255, required=True)
    mobile = serializers.CharField(max_length=20, required=True)
    
    def validate_mobile(self, value):
        """Validate mobile number uniqueness"""
        if User.objects.filter(mobile=value).exists():
            raise serializers.ValidationError("این شماره تلفن قبلاً ثبت شده است")
        return value
    
    def validate_company_id(self, value):
        """Validate company exists"""
        if not Company.objects.filter(id=value).exists():
            raise serializers.ValidationError("شرکت یافت نشد")
        return value


class UserLoginSerializer(serializers.Serializer):
    """Serializer for token-based login (passwordless)."""
    mobile = serializers.CharField(max_length=20, required=True)
    token = serializers.UUIDField(required=True, write_only=True)


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Custom JWT serializer that accepts mobile + API token UUID (passwordless)."""
    mobile = serializers.CharField()
    token = serializers.UUIDField(write_only=True)
    username = None  # Remove username field
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Remove username field if it exists and ensure mobile exists
        if 'username' in self.fields:
            del self.fields['username']
        if 'password' in self.fields:
            del self.fields['password']
        if 'mobile' not in self.fields:
            self.fields['mobile'] = serializers.CharField()
        if 'token' not in self.fields:
            self.fields['token'] = serializers.UUIDField(write_only=True)
    
    def validate(self, attrs):
        # Get mobile from attrs (or from username if it exists)
        mobile = attrs.get('mobile') or attrs.get('username')
        token_uuid = attrs.get('token') or attrs.get('password')
        
        if not mobile or not token_uuid:
            raise serializers.ValidationError('شماره تلفن و توکن الزامی است')
        
        # Find user by mobile
        try:
            user = User.objects.get(mobile=mobile)
        except User.DoesNotExist:
            raise serializers.ValidationError('شماره تلفن یا توکن اشتباه است')
        
        # Check token belongs to this user
        if not Token.objects.filter(uuid=token_uuid, user=user).exists():
            raise serializers.ValidationError('شماره تلفن یا توکن اشتباه است')
        
        # Generate token using parent method
        refresh = self.get_token(user)
        
        # Add custom claims to JWT payload
        refresh['user_id'] = user.id
        refresh['company_id'] = user.company_id
        refresh['name'] = user.name
        refresh['mobile'] = user.mobile
        
        # Add role information
        user_roles = user.user_roles.select_related('role').all()
        roles = [ur.role.title for ur in user_roles]
        refresh['role'] = roles[0] if roles else None
        refresh['roles'] = roles
        refresh['is_admin'] = 'admin' in [r.lower() for r in roles]
        
        # Add permissions (using role-based permissions for now)
        # Since we don't use Django Groups/Permissions, we'll use role-based permissions
        permissions = []
        if refresh['is_admin']:
            permissions.extend(['admin.read', 'admin.write', 'admin.delete'])
        refresh['permissions'] = list(set(permissions))  # Remove duplicates
        
        data = {}
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        
        return data


class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = '__all__'


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = '__all__'


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'


class UserRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRole
        fields = '__all__'

