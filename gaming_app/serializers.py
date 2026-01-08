from rest_framework import serializers
from .models import Level, UserLevel, Badge, UserBadge, UserPoint, UserAction


class LevelSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source='company.name', read_only=True)
    user_levels_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Level
        fields = '__all__'
    
    def get_user_levels_count(self, obj):
        """تعداد کاربرانی که به این سطح رسیده‌اند"""
        return obj.user_levels.count()


class UserLevelSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.name', read_only=True)
    user_mobile = serializers.CharField(source='user.mobile', read_only=True)
    level_details = LevelSerializer(source='level', read_only=True)
    
    class Meta:
        model = UserLevel
        fields = '__all__'
        read_only_fields = ['id', 'reachedat']


class BadgeSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source='company.name', read_only=True)
    mission_title = serializers.CharField(source='mission.title', read_only=True)
    user_badges_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Badge
        fields = '__all__'
    
    def get_user_badges_count(self, obj):
        """تعداد کاربرانی که این نشان را کسب کرده‌اند"""
        return obj.user_badges.count()


class UserBadgeSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.name', read_only=True)
    user_mobile = serializers.CharField(source='user.mobile', read_only=True)
    badge_details = BadgeSerializer(source='badge', read_only=True)
    
    class Meta:
        model = UserBadge
        fields = '__all__'
        read_only_fields = ['id', 'earnedat']


class UserPointSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.name', read_only=True)
    user_mobile = serializers.CharField(source='user.mobile', read_only=True)
    
    class Meta:
        model = UserPoint
        fields = '__all__'
        read_only_fields = ['id', 'lastupdated']


class UserActionSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.name', read_only=True)
    user_mobile = serializers.CharField(source='user.mobile', read_only=True)
    
    class Meta:
        model = UserAction
        fields = '__all__'
        read_only_fields = ['id', 'createdat']
