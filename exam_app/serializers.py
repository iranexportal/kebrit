from rest_framework import serializers
from .models import Evaluation, Question, Quiz, QuizResponse, QuizResponseEvaluation


class EvaluationSerializer(serializers.ModelSerializer):
    questions_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Evaluation
        fields = '__all__'
    
    def get_questions_count(self, obj):
        """تعداد سوالات موجود در بانک سوالات این evaluation"""
        return obj.questions.count()


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'
        read_only_fields = ['id']


class QuestionForQuizSerializer(serializers.ModelSerializer):
    """Serializer برای نمایش سوالات در کوئیز (بدون نمایش پاسخ صحیح)"""
    class Meta:
        model = Question
        fields = ['id', 'description', 'img', 'type', 'c1', 'c2', 'c3', 'c4', 'weight', 'can_shuffle']
        read_only_fields = ['id']


class QuizSerializer(serializers.ModelSerializer):
    evaluation_details = EvaluationSerializer(source='evaluation', read_only=True)
    questions = serializers.SerializerMethodField()
    responses_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Quiz
        fields = '__all__'
        read_only_fields = ['id', 'start_at', 'end_at', 'score', 'is_accept', 'state']
    
    def get_questions(self, obj):
        """سوالات انتخاب شده برای این کوئیز"""
        questions = Question.objects.filter(
            quiz_responses__quiz=obj
        ).distinct()
        return QuestionForQuizSerializer(questions, many=True).data
    
    def get_responses_count(self, obj):
        """تعداد پاسخ‌های ثبت شده"""
        return obj.responses.count()


class QuizResponseSerializer(serializers.ModelSerializer):
    question_details = QuestionSerializer(source='question', read_only=True)
    
    class Meta:
        model = QuizResponse
        fields = '__all__'
        read_only_fields = ['id', 'score']


class QuizResponseSubmitSerializer(serializers.Serializer):
    """Serializer برای ارسال پاسخ‌های کوئیز"""
    question_id = serializers.IntegerField(required=True)
    answer = serializers.IntegerField(required=True, allow_null=True)
    done = serializers.CharField(required=False, allow_null=True, allow_blank=True)


class QuizSubmitSerializer(serializers.Serializer):
    """Serializer برای ارسال تمام پاسخ‌های یک کوئیز"""
    quiz_id = serializers.IntegerField(required=True)
    responses = QuizResponseSubmitSerializer(many=True, required=True)


class QuizResponseEvaluationSerializer(serializers.ModelSerializer):
    quiz_response_details = QuizResponseSerializer(source='quiz_response', read_only=True)
    user_name = serializers.CharField(source='user.name', read_only=True)
    
    class Meta:
        model = QuizResponseEvaluation
        fields = '__all__'
        read_only_fields = ['id', 'score']


class QuizResultSerializer(serializers.Serializer):
    """Serializer برای نمایش نتیجه نهایی کوئیز"""
    quiz_id = serializers.IntegerField()
    total_questions = serializers.IntegerField()
    correct_answers = serializers.IntegerField()
    wrong_answers = serializers.IntegerField()
    percentage = serializers.FloatField()
    total_score = serializers.FloatField()
    is_accept = serializers.BooleanField()
    responses = QuizResponseSerializer(many=True)

