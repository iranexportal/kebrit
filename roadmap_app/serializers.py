from rest_framework import serializers
from .models import Mission, MissionRelation, MissionResult, Ability


class MissionSerializer(serializers.ModelSerializer):
    evaluation_results = serializers.SerializerMethodField()
    
    class Meta:
        model = Mission
        fields = '__all__'
    
    def get_evaluation_results(self, obj):
        """نتایج آزمون‌های مرتبط با این ماموریت"""
        request = self.context.get('request')
        if not request or not request.user or not request.user.is_authenticated:
            return []
        
        # Import در اینجا برای جلوگیری از circular import
        from exam_app.models import Evaluation, QuizResponseEvaluation
        
        # پیدا کردن Evaluation های مرتبط با این Mission
        evaluations = Evaluation.objects.filter(
            mission=obj,
            is_active=True
        ).select_related('type')
        
        results = []
        for evaluation in evaluations:
            # پیدا کردن آخرین QuizResponseEvaluation برای این کاربر و evaluation
            quiz_evaluation = QuizResponseEvaluation.objects.filter(
                user=request.user,
                quiz__evaluation=evaluation,
                quiz__end_at__isnull=False
            ).select_related('quiz', 'quiz__evaluation', 'quiz__evaluation__type').order_by('-quiz__end_at').first()
            
            if quiz_evaluation:
                results.append({
                    'evaluation_id': evaluation.id,
                    'evaluation_title': evaluation.title,
                    'evaluation_type': evaluation.type.title if evaluation.type else None,
                    'quiz_id': quiz_evaluation.quiz_id,
                    'score': round(quiz_evaluation.score, 2) if quiz_evaluation.score is not None else None,
                    'quiz_start_at': quiz_evaluation.quiz.start_at.isoformat() if quiz_evaluation.quiz.start_at else None,
                    'quiz_end_at': quiz_evaluation.quiz.end_at.isoformat() if quiz_evaluation.quiz.end_at else None,
                    'is_accept': quiz_evaluation.quiz.is_accept,
                    'accept_score': evaluation.accept_score,
                })
        
        return results


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


class UserMissionQuerySerializer(serializers.Serializer):
    mobile = serializers.CharField(required=True, help_text="شماره تلفن کاربر")
    company_id = serializers.IntegerField(required=True, help_text="شناسه شرکت")

