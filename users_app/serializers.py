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
        extra_kwargs = {'password': {'write_only': True}}


class UserCreateSerializer(serializers.Serializer):
    """Serializer for creating a new user with auto-generated password"""
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
    """Serializer for user login with mobile and password"""
    mobile = serializers.CharField(max_length=20, required=True)
    password = serializers.CharField(max_length=255, required=True, write_only=True)


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Custom JWT serializer that accepts mobile instead of username"""
    mobile = serializers.CharField()
    username = None  # Remove username field
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Remove username field if it exists and ensure mobile exists
        if 'username' in self.fields:
            del self.fields['username']
        if 'mobile' not in self.fields:
            self.fields['mobile'] = serializers.CharField()
    
    def validate(self, attrs):
        # Get mobile from attrs (or from username if it exists)
        mobile = attrs.get('mobile') or attrs.get('username')
        password = attrs.get('password')
        
        if not mobile or not password:
            raise serializers.ValidationError('شماره تلفن و رمز عبور الزامی است')
        
        # Find user by mobile
        try:
            user = User.objects.get(mobile=mobile)
        except User.DoesNotExist:
            raise serializers.ValidationError('شماره تلفن یا رمز عبور اشتباه است')
        
        # Check password (plain text comparison since we store plain passwords)
        if user.password != password:
            raise serializers.ValidationError('شماره تلفن یا رمز عبور اشتباه است')
        
        # Generate token using parent method
        refresh = self.get_token(user)
        
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

