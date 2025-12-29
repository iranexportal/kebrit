from django.contrib import admin
from .models import Evaluation, Question, Quiz, QuizResponse, QuizResponseEvaluation


@admin.register(Evaluation)
class EvaluationAdmin(admin.ModelAdmin):
    list_display = ['id', 'type', 'accept_score', 'number_of_question', 'mission', 'user', 'is_active', 'create_at']
    list_filter = ['type', 'is_active', 'can_back', 'create_at']
    search_fields = ['mission__title', 'user__name']
    raw_id_fields = ['mission', 'user']
    date_hierarchy = 'create_at'


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['id', 'evaluation', 'type', 'weight', 'correct']
    list_filter = ['type', 'evaluation', 'can_shuffle']
    search_fields = ['description']
    raw_id_fields = ['evaluation']


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ['id', 'evaluation', 'user', 'start_at', 'end_at', 'score', 'is_accept', 'state']
    list_filter = ['is_accept', 'state', 'start_at']
    search_fields = ['evaluation__mission__title', 'user__name']
    raw_id_fields = ['evaluation', 'user']
    date_hierarchy = 'start_at'


@admin.register(QuizResponse)
class QuizResponseAdmin(admin.ModelAdmin):
    list_display = ['id', 'quiz', 'question', 'answer', 'score', 'done']
    list_filter = ['quiz', 'question']
    search_fields = ['quiz__id', 'question__description']
    raw_id_fields = ['quiz', 'question']


@admin.register(QuizResponseEvaluation)
class QuizResponseEvaluationAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'quiz_response', 'score']
    list_filter = ['user']
    search_fields = ['user__name', 'quiz_response__id']
    raw_id_fields = ['user', 'quiz_response']
