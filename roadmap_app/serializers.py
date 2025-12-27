from rest_framework import serializers
from .models import Mission, MissionRelation, MissionResult, Ability


class MissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mission
        fields = '__all__'


class MissionRelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = MissionRelation
        fields = '__all__'


class MissionResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = MissionResult
        fields = '__all__'


class AbilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Ability
        fields = '__all__'

