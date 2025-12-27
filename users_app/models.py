from django.db import models


class Company(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'users.company'
        managed = True
        app_label = 'users_app'

    def __str__(self):
        return self.name


class User(models.Model):
    id = models.AutoField(primary_key=True)
    uuid = models.CharField(max_length=255)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, db_column='companyId', related_name='users')
    mobile = models.CharField(max_length=20)
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'users.user'
        managed = True
        app_label = 'users_app'
        indexes = [
            models.Index(fields=['company'], name='idx_user_companyId'),
        ]

    @property
    def is_authenticated(self):
        """Required for Django authentication"""
        return True

    def __str__(self):
        return self.name


class Session(models.Model):
    uuid = models.UUIDField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='userId', related_name='sessions')
    expier_at = models.DateTimeField(db_column='expierAt')

    class Meta:
        db_table = 'users.session'
        managed = True
        app_label = 'users_app'

    def __str__(self):
        return str(self.uuid)


class Token(models.Model):
    uuid = models.UUIDField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='userId', related_name='tokens')

    class Meta:
        db_table = 'users.token'
        managed = True
        app_label = 'users_app'

    def __str__(self):
        return str(self.uuid)


class Role(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, db_column='companyId', related_name='roles')

    class Meta:
        db_table = 'users.role'
        managed = True
        app_label = 'users_app'
        indexes = [
            models.Index(fields=['company'], name='idx_role_companyId'),
        ]

    def __str__(self):
        return self.title


class UserRole(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='userId', related_name='user_roles')
    role = models.ForeignKey(Role, on_delete=models.CASCADE, db_column='roleId', related_name='user_roles')

    class Meta:
        db_table = 'users.userRole'
        managed = True
        app_label = 'users_app'
        indexes = [
            models.Index(fields=['user'], name='idx_userRole_userId'),
            models.Index(fields=['role'], name='idx_userRole_roleId'),
        ]

    def __str__(self):
        return f"{self.user.name} - {self.role.title}"
