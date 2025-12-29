from django.contrib import admin
from .models import Company, User, Session, Token, Role, UserRole


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'uuid', 'name', 'mobile', 'company']
    list_filter = ['company']
    search_fields = ['name', 'mobile', 'uuid']
    raw_id_fields = ['company']


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ['uuid', 'user', 'expier_at']
    list_filter = ['expier_at']
    search_fields = ['uuid']
    raw_id_fields = ['user']


@admin.register(Token)
class TokenAdmin(admin.ModelAdmin):
    list_display = ['uuid', 'user']
    search_fields = ['uuid']
    raw_id_fields = ['user']


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'company']
    list_filter = ['company']
    search_fields = ['title']
    raw_id_fields = ['company']


@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'role']
    list_filter = ['role']
    search_fields = ['user__name', 'role__title']
    raw_id_fields = ['user', 'role']
