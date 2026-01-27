from rest_framework import serializers


class MissionReportRequestSerializer(serializers.Serializer):
    mobile = serializers.CharField(required=True, help_text="شماره تلفن دانشجو")
    mission_id = serializers.IntegerField(required=True, help_text="شناسه ماموریت")


class MissionAttemptSerializer(serializers.Serializer):
    evaluation_id = serializers.IntegerField()
    quiz_id = serializers.IntegerField()
    percentage = serializers.FloatField(allow_null=True)
    total_score = serializers.FloatField(allow_null=True)
    is_accept = serializers.BooleanField(allow_null=True)
    accept_score = serializers.IntegerField(allow_null=True)
    start_at = serializers.DateTimeField(allow_null=True)
    end_at = serializers.DateTimeField(allow_null=True)


class MissionReportSerializer(serializers.Serializer):
    mission_id = serializers.IntegerField()
    mobile = serializers.CharField()
    user_id = serializers.IntegerField()
    attempts = MissionAttemptSerializer(many=True)


