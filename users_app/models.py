from pickle import FALSE
from django.db import models
from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    """Custom manager for User model with get_by_natural_key support"""
    
    def get_by_natural_key(self, mobile):
        """Retrieve user by mobile number (natural key)"""
        return self.get(mobile=mobile)


class Company(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'company'
        managed = False
        app_label = 'users_app'

    def __str__(self):
        return self.name


class User(models.Model):
    id = models.AutoField(primary_key=True)
    uuid = models.CharField(max_length=255)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, db_column='companyid', related_name='users')
    mobile = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=255)
    
    # Custom manager
    objects = UserManager()
    
    # Required for Django authentication system
    USERNAME_FIELD = 'mobile'
    REQUIRED_FIELDS = ['name', 'company']
    
    @property
    def is_active(self):
        """Always return True since is_active column doesn't exist in DB"""
        return True
    
    @property
    def is_staff(self):
        """Check if user has admin role (required for Django admin access)"""
        try:
            # Check if user_roles is already prefetched or cached
            if hasattr(self, '_prefetched_objects_cache') and 'user_roles' in self._prefetched_objects_cache:
                user_roles = self._prefetched_objects_cache['user_roles']
            else:
                user_roles = self.user_roles.select_related('role').all()
            return any(ur.role.title.lower() == 'admin' for ur in user_roles)
        except (AttributeError, Exception):
            return False
    
    @property
    def is_superuser(self):
        """Check if user is superuser (admin role)"""
        return self.is_staff

    class Meta:
        db_table = 'user'
        managed = False
        app_label = 'users_app'
        indexes = [
            models.Index(fields=['company'], name='idx_user_companyId'),
        ]

    @property
    def is_authenticated(self):
        """Required for Django authentication"""
        return True
    
    @property
    def is_anonymous(self):
        """Required for Django authentication"""
        return False
    
    def check_password(self, raw_password):
        """Check password (plain text comparison since we store plain passwords)"""
        return self.password == raw_password
    
    def set_password(self, raw_password):
        """Set password (plain text storage)"""
        self.password = raw_password
    
    def get_username(self):
        """Return the username (mobile) for this user"""
        return self.mobile
    
    def has_perm(self, perm, obj=None):
        """Check if user has a specific permission"""
        # Superusers have all permissions
        if self.is_superuser:
            return True
        # For now, only admin users have permissions
        return self.is_staff
    
    def has_module_perms(self, app_label):
        """Check if user has permissions for a specific app"""
        # Superusers have all module permissions
        if self.is_superuser:
            return True
        # For now, only admin users have module permissions
        return self.is_staff

    def __str__(self):
        return self.name


class Session(models.Model):
    uuid = models.UUIDField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='userid', related_name='sessions')
    expier_at = models.DateTimeField(db_column='expierat')

    class Meta:
        db_table = 'session'
        managed = False
        app_label = 'users_app'

    def __str__(self):
        return str(self.uuid)


class Token(models.Model):
    uuid = models.UUIDField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='userid', related_name='tokens')

    class Meta:
        db_table = 'token'
        managed = False
        app_label = 'users_app'

    def __str__(self):
        return str(self.uuid)


class Role(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, db_column='companyid', related_name='roles')

    class Meta:
        db_table = 'role'
        managed = False
        app_label = 'users_app'
        indexes = [
            models.Index(fields=['company'], name='idx_role_companyId'),
        ]

    def __str__(self):
        return self.title


class UserRole(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='userid', related_name='user_roles')
    role = models.ForeignKey(Role, on_delete=models.CASCADE, db_column='roleid', related_name='user_roles')

    class Meta:
        db_table = 'userrole'
        managed = False
        app_label = 'users_app'
        indexes = [
            models.Index(fields=['user'], name='idx_userRole_userId'),
            models.Index(fields=['role'], name='idx_userRole_roleId'),
        ]

    def __str__(self):
        return f"{self.user.name} - {self.role.title}"
