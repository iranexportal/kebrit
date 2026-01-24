from rest_framework import serializers


class ClientExamLaunchSerializer(serializers.Serializer):
    """
    Customer -> API payload for starting an exam session for a student.
    """

    student_uuid = serializers.CharField(max_length=255, required=True)
    mobile = serializers.CharField(max_length=20, required=True)
    eurl = serializers.IntegerField(required=True)  # evaluation id
    callback_url = serializers.URLField(required=True, max_length=2000)
    name = serializers.CharField(max_length=255, required=False, allow_blank=True)


class LaunchAnswerSerializer(serializers.Serializer):
    question_id = serializers.IntegerField(required=True)
    answer = serializers.CharField(required=True, allow_null=True, allow_blank=True)
    done = serializers.CharField(required=False, allow_null=True, allow_blank=True)


class LaunchSubmitSerializer(serializers.Serializer):
    """
    Student -> API payload for submitting the whole quiz at the end.
    Same structure as existing quiz submit, but without quiz_id (derived from launch).
    """

    responses = LaunchAnswerSerializer(many=True, required=True)

