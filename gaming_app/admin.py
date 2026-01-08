from django.contrib import admin
from django.utils.html import format_html
from .models import Level, UserLevel, Badge, UserBadge, UserPoint, UserAction


@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    list_display = ['id', 'code', 'order', 'title', 'requiredpoints', 'company', 'isactive', 'user_levels_count']
    list_filter = ['isactive', 'code', 'company']
    search_fields = ['title', 'code', 'description', 'company__name']
    raw_id_fields = ['company']
    list_editable = ['isactive', 'order']
    ordering = ['order']
    
    fieldsets = (
        ('اطلاعات پایه', {
            'fields': ('id', 'code', 'order', 'title', 'description', 'isactive')
        }),
        ('تنظیمات', {
            'fields': ('requiredpoints', 'icon')
        }),
        ('ارتباطات', {
            'fields': ('company',)
        }),
    )
    
    def user_levels_count(self, obj):
        """تعداد کاربرانی که به این سطح رسیده‌اند"""
        count = obj.user_levels.count()
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            'green' if count > 0 else 'gray',
            count
        )
    user_levels_count.short_description = 'تعداد کاربران'


@admin.register(UserLevel)
class UserLevelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'level', 'currentpoints', 'reachedat']
    list_filter = ['level', 'reachedat', 'user__company']
    search_fields = ['user__name', 'user__mobile', 'level__title', 'level__code']
    raw_id_fields = ['user', 'level']
    readonly_fields = ['id', 'reachedat']
    date_hierarchy = 'reachedat'
    ordering = ['-reachedat', '-id']
    
    fieldsets = (
        ('اطلاعات پایه', {
            'fields': ('id', 'user', 'level')
        }),
        ('اطلاعات سطح', {
            'fields': ('currentpoints', 'reachedat')
        }),
    )


@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ['id', 'code', 'title', 'mission', 'company', 'isactive', 'user_badges_count']
    list_filter = ['isactive', 'code', 'company']
    search_fields = ['title', 'code', 'description', 'mission__title', 'company__name']
    raw_id_fields = ['company', 'mission']
    list_editable = ['isactive']
    ordering = ['id']
    
    fieldsets = (
        ('اطلاعات پایه', {
            'fields': ('id', 'code', 'title', 'description', 'isactive')
        }),
        ('تنظیمات', {
            'fields': ('icon',)
        }),
        ('ارتباطات', {
            'fields': ('mission', 'company')
        }),
    )
    
    def user_badges_count(self, obj):
        """تعداد کاربرانی که این نشان را کسب کرده‌اند"""
        count = obj.user_badges.count()
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            'green' if count > 0 else 'gray',
            count
        )
    user_badges_count.short_description = 'تعداد کاربران'


@admin.register(UserBadge)
class UserBadgeAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'badge', 'earnedat']
    list_filter = ['badge', 'earnedat', 'user__company']
    search_fields = ['user__name', 'user__mobile', 'badge__title', 'badge__code']
    raw_id_fields = ['user', 'badge']
    readonly_fields = ['id', 'earnedat']
    date_hierarchy = 'earnedat'
    ordering = ['-earnedat', '-id']
    
    fieldsets = (
        ('اطلاعات پایه', {
            'fields': ('id', 'user', 'badge')
        }),
        ('اطلاعات کسب', {
            'fields': ('earnedat',)
        }),
    )


@admin.register(UserPoint)
class UserPointAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'totalpoints', 'lastupdated', 'points_display']
    list_filter = ['lastupdated', 'user__company']
    search_fields = ['user__name', 'user__mobile']
    raw_id_fields = ['user']
    readonly_fields = ['id', 'lastupdated']
    ordering = ['-totalpoints', '-id']
    
    fieldsets = (
        ('اطلاعات پایه', {
            'fields': ('id', 'user')
        }),
        ('امتیازات', {
            'fields': ('totalpoints', 'lastupdated')
        }),
    )
    
    def points_display(self, obj):
        """نمایش امتیاز با رنگ"""
        if obj.totalpoints is not None:
            color = 'green' if obj.totalpoints > 0 else 'gray'
            return format_html(
                '<span style="color: {}; font-weight: bold; font-size: 14px;">{:,}</span>',
                color,
                obj.totalpoints
            )
        return '-'
    points_display.short_description = 'امتیاز'


@admin.register(UserAction)
class UserActionAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'actiontype', 'pointsearned', 'points_display', 'createdat']
    list_filter = ['actiontype', 'createdat', 'user__company']
    search_fields = ['user__name', 'user__mobile', 'actiontype', 'description']
    raw_id_fields = ['user']
    readonly_fields = ['id', 'createdat']
    date_hierarchy = 'createdat'
    ordering = ['-createdat', '-id']
    
    fieldsets = (
        ('اطلاعات پایه', {
            'fields': ('id', 'user', 'actiontype')
        }),
        ('جزئیات', {
            'fields': ('pointsearned', 'description', 'createdat')
        }),
    )
    
    def points_display(self, obj):
        """نمایش امتیاز با رنگ"""
        if obj.pointsearned is not None:
            color = 'green' if obj.pointsearned > 0 else 'orange' if obj.pointsearned == 0 else 'red'
            return format_html(
                '<span style="color: {}; font-weight: bold;">{}</span>',
                color,
                obj.pointsearned
            )
        return '-'
    points_display.short_description = 'امتیاز'
