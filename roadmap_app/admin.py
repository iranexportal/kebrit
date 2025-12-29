from django.contrib import admin
from .models import Mission, MissionRelation, MissionResult, Ability


@admin.register(Mission)
class MissionAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'type', 'company', 'user', 'point', 'is_active', 'create_at']
    list_filter = ['type', 'is_active', 'company', 'create_at']
    search_fields = ['title', 'content']
    raw_id_fields = ['company', 'user']
    date_hierarchy = 'create_at'


@admin.register(MissionRelation)
class MissionRelationAdmin(admin.ModelAdmin):
    list_display = ['id', 'mission', 'parent', 'child']
    list_filter = ['mission']
    search_fields = ['mission__title']
    raw_id_fields = ['mission', 'parent', 'child']


@admin.register(Ability)
class AbilityAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'company']
    list_filter = ['company']
    search_fields = ['title']
    raw_id_fields = ['company']


@admin.register(MissionResult)
class MissionResultAdmin(admin.ModelAdmin):
    list_display = ['id', 'mission', 'user', 'state', 'user_grant', 'quiz_id']
    list_filter = ['state', 'mission', 'user']
    search_fields = ['mission__title', 'user__name']
    raw_id_fields = ['mission', 'user', 'ability']
