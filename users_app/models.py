from pickle import FALSE
from django.db import models
from django.contrib.auth.models import BaseUserManager
from django.conf import settings
from django.utils.crypto import salted_hmac
import uuid as _uuid


class UserManager(BaseUserManager):
    """Custom manager for User model with get_by_natural_key support"""
    
    def get_by_natural_key(self, username):
        """Retrieve user by username (natural key)"""
        return self.get(username=username)

    def create_user(self, username, company, name=None, mobile=None, **extra_fields):
        """
        Create a passwordless user.

        Notes:
        - We don't store passwords.
        - `company` can be a Company instance or a company id.
        """
        if not username:
            raise ValueError("The username must be set")
        if not company:
            raise ValueError("The company must be set")

        if isinstance(company, int):
            company = Company.objects.get(pk=company)

        user_uuid = extra_fields.pop("uuid", None) or str(_uuid.uuid4())
        mobile = mobile or username  # mobile is required by current DB schema
        name = name or username

        user = self.model(
            username=username,
            uuid=user_uuid,
            company=company,
            mobile=mobile,
            name=name,
            **extra_fields,
        )
        user.save(using=self._db)
        return user

    def create_superuser(self, username, company, name=None, mobile=None, **extra_fields):
        """
        Create an admin user:
        - creates the user (passwordless)
        - ensures 'admin' role exists for the company
        - assigns admin role to user (so Django admin works via is_staff property)
        - creates an API Token for admin login (used as "password" in admin login form)
        """
        user = self.create_user(username=username, company=company, name=name, mobile=mobile, **extra_fields)

        # Ensure role + mapping
        role, _ = Role.objects.get_or_create(company=user.company, title="admin")
        UserRole.objects.get_or_create(user=user, role=role)

        # Ensure at least one token for login
        Token.objects.get_or_create(user=user, defaults={"uuid": _uuid.uuid4()})

        return user


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
    username = models.CharField('username', max_length=150, null=True, blank=True, unique=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, db_column='companyid', related_name='users')
    mobile = models.CharField(max_length=20)
    name = models.CharField(max_length=100)
    
    # Custom manager
    objects = UserManager()
    
    # Required for Django authentication system
    USERNAME_FIELD = 'username'
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
    
    def get_username(self):
        """Return the username for this user (fallback to mobile)"""
        return self.username or self.mobile

    # --- Passwordless user compatibility helpers (admin/auth expects these) ---
    def set_password(self, raw_password):
        """
        No-op. We intentionally do NOT store passwords.

        Django's default ModelBackend calls set_password() as part of a timing-attack mitigation.
        We keep this method to avoid crashes if something calls it.
        """
        return None

    def check_password(self, raw_password):
        """Always False: password auth is not supported."""
        return False

    def get_session_auth_hash(self):
        """
        Return a stable hash used by Django sessions.
        Since we don't have passwords, we base it on immutable identifiers.
        """
        value = f"{self.pk}:{self.uuid}:{self.company_id}"
        return salted_hmac("users_app.User", value, secret=settings.SECRET_KEY).hexdigest()
    
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
