from rest_framework import serializers
from .models import Evaluation, Question, Quiz, QuizResponse, QuizResponseEvaluation


class EvaluationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evaluation
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'


class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = '__all__'


class QuizResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizResponse
        fields = '__all__'


class QuizResponseEvaluationSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizResponseEvaluation
        fields = '__all__'

