from rest_framework import serializers
from .models import Evaluation, Question, Quiz, QuizResponse, QuizResponseEvaluation


class EvaluationSerializer(serializers.ModelSerializer):
    questions_count = serializers.SerializerMethodField()
    last_score = serializers.SerializerMethodField()
    last_quiz_id = serializers.SerializerMethodField()
    
    class Meta:
        model = Evaluation
        fields = '__all__'
    
    def get_questions_count(self, obj):
        """تعداد سوالات موجود در بانک سوالات این evaluation"""
        return obj.questions.count()
    
    def _get_last_evaluation_data(self, obj):
        """کش کردن آخرین evaluation برای جلوگیری از query های تکراری"""
        if not hasattr(obj, '_last_evaluation_cache'):
            request = self.context.get('request')
            if not request or not request.user or not request.user.is_authenticated:
                obj._last_evaluation_cache = None
            else:
                try:
                    # پیدا کردن آخرین QuizResponseEvaluation که quiz آن تمام شده باشد
                    last_evaluation = QuizResponseEvaluation.objects.filter(
                        user=request.user,
                        quiz__evaluation=obj,
                        quiz__end_at__isnull=False
                    ).select_related('quiz').order_by('-quiz__end_at').first()
                    
                    obj._last_evaluation_cache = last_evaluation
                except Exception:
                    obj._last_evaluation_cache = None
        return obj._last_evaluation_cache
    
    def get_last_score(self, obj):
        """نمره آخرین آزمون کاربر برای این evaluation (percentage)"""
        last_evaluation = self._get_last_evaluation_data(obj)
        if last_evaluation and last_evaluation.score is not None:
            return round(last_evaluation.score, 2)
        return None
    
    def get_last_quiz_id(self, obj):
        """شناسه آخرین کوئیز کاربر برای این evaluation"""
        last_evaluation = self._get_last_evaluation_data(obj)
        if last_evaluation:
            return last_evaluation.quiz_id
        return None


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
    evaluation_details = serializers.SerializerMethodField()
    questions = serializers.SerializerMethodField()
    responses_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Quiz
        fields = '__all__'
        read_only_fields = ['id', 'start_at', 'end_at', 'score', 'is_accept', 'state']
    
    def get_evaluation_details(self, obj):
        """جزئیات evaluation با context برای نمایش نمره قبلی"""
        return EvaluationSerializer(obj.evaluation, context=self.context).data
    
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
    quiz_details = QuizSerializer(source='quiz', read_only=True)
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

