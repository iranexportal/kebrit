from django.contrib import admin
from django.utils.html import format_html
from .models import EvaluationType, Evaluation, Question, Quiz, QuizResponse, QuizResponseEvaluation


@admin.register(EvaluationType)
class EvaluationTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'evaluations_count']
    search_fields = ['title']
    list_display_links = ['id', 'title']
    ordering = ['id']
    
    def evaluations_count(self, obj):
        """تعداد ارزیابی‌های مرتبط با این نوع"""
        count = obj.evaluations.count()
        return format_html(
            '<span style="color: {};">{}</span>',
            'green' if count > 0 else 'gray',
            count
        )
    evaluations_count.short_description = 'تعداد ارزیابی‌ها'


@admin.register(Evaluation)
class EvaluationAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'type', 'accept_score', 'number_of_question', 'questions_count', 'mission', 'user', 'is_active', 'can_back', 'duration', 'create_at']
    list_filter = ['type', 'is_active', 'can_back', 'create_at', 'mission']
    search_fields = ['title', 'mission__title', 'user__name', 'type__title', 'user__mobile']
    raw_id_fields = ['type', 'mission', 'user']
    date_hierarchy = 'create_at'
    list_editable = ['is_active', 'can_back']
    readonly_fields = ['id', 'create_at', 'questions_count_display']
    ordering = ['-create_at', '-id']
    
    fieldsets = (
        ('اطلاعات پایه', {
            'fields': ('id', 'title', 'type', 'is_active')
        }),
        ('تنظیمات ارزیابی', {
            'fields': ('accept_score', 'number_of_question', 'duration', 'can_back')
        }),
        ('ارتباطات', {
            'fields': ('mission', 'user')
        }),
        ('اطلاعات تکمیلی', {
            'fields': ('questions_count_display', 'create_at'),
            'classes': ('collapse',)
        }),
    )
    
    def questions_count(self, obj):
        """تعداد سوالات در لیست"""
        count = obj.questions.count()
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            'blue' if count > 0 else 'gray',
            count
        )
    questions_count.short_description = 'سوالات'
    
    def questions_count_display(self, obj):
        """تعداد سوالات در صفحه جزئیات"""
        if obj.pk:
            count = obj.questions.count()
            return format_html(
                '<strong style="color: blue; font-size: 14px;">{} سوال</strong>',
                count
            )
        return 'هنوز ذخیره نشده'
    questions_count_display.short_description = 'تعداد سوالات'


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['id', 'evaluation', 'type_display', 'weight', 'correct', 'can_shuffle', 'preview']
    list_filter = ['type', 'evaluation', 'can_shuffle', 'evaluation__type']
    search_fields = ['description', 'evaluation__title', 'evaluation__id']
    raw_id_fields = ['evaluation']
    list_editable = ['can_shuffle']
    readonly_fields = ['id', 'preview_full']
    ordering = ['evaluation', 'id']
    
    fieldsets = (
        ('اطلاعات پایه', {
            'fields': ('id', 'evaluation', 'type', 'weight', 'can_shuffle')
        }),
        ('متن سوال', {
            'fields': ('description', 'img', 'preview_full')
        }),
        ('گزینه‌های چندگزینه‌ای', {
            'fields': ('c1', 'c2', 'c3', 'c4', 'correct'),
            'classes': ('collapse',)
        }),
        ('پاسخ تشریحی', {
            'fields': ('answer',),
            'classes': ('collapse',)
        }),
    )
    
    def type_display(self, obj):
        """نمایش نوع سوال"""
        return format_html(
            '<span style="color: {};">{}</span>',
            'green' if obj.type else 'orange',
            'چندگزینه‌ای' if obj.type else 'تشریحی'
        )
    type_display.short_description = 'نوع'
    
    def preview(self, obj):
        """پیش‌نمایش کوتاه سوال"""
        if obj.description:
            preview_text = obj.description[:50] + '...' if len(obj.description) > 50 else obj.description
            return format_html('<span title="{}">{}</span>', obj.description, preview_text)
        return '-'
    preview.short_description = 'پیش‌نمایش'
    
    def preview_full(self, obj):
        """پیش‌نمایش کامل سوال"""
        if obj.description:
            return format_html('<div style="padding: 10px; background: #f5f5f5; border-radius: 5px;">{}</div>', obj.description)
        return '-'
    preview_full.short_description = 'متن کامل سوال'


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ['id', 'evaluation', 'user', 'start_at', 'end_at', 'score_display', 'is_accept_display', 'state', 'duration_display']
    list_filter = ['is_accept', 'state', 'start_at', 'evaluation__type']
    search_fields = ['evaluation__title', 'evaluation__mission__title', 'user__name', 'user__mobile', 'id']
    raw_id_fields = ['evaluation', 'user']
    date_hierarchy = 'start_at'
    readonly_fields = ['id', 'start_at', 'end_at', 'score', 'is_accept', 'state', 'duration_calc']
    ordering = ['-start_at', '-id']
    
    fieldsets = (
        ('اطلاعات پایه', {
            'fields': ('id', 'evaluation', 'user')
        }),
        ('زمان‌بندی', {
            'fields': ('start_at', 'end_at', 'duration_calc')
        }),
        ('نتایج', {
            'fields': ('score', 'is_accept', 'state')
        }),
    )
    
    def score_display(self, obj):
        """نمایش نمره با رنگ"""
        if obj.score is not None:
            color = 'green' if obj.is_accept else 'red'
            return format_html(
                '<span style="color: {}; font-weight: bold;">{:.2f}</span>',
                color,
                obj.score
            )
        return '-'
    score_display.short_description = 'نمره'
    
    def is_accept_display(self, obj):
        """نمایش وضعیت قبولی"""
        if obj.is_accept is None:
            return format_html('<span style="color: gray;">-</span>')
        if obj.is_accept:
            return format_html('<span style="color: green; font-weight: bold;">✓ قبول</span>')
        return format_html('<span style="color: red; font-weight: bold;">✗ رد</span>')
    is_accept_display.short_description = 'وضعیت'
    
    def duration_display(self, obj):
        """نمایش مدت زمان آزمون"""
        if obj.end_at and obj.start_at:
            duration = obj.end_at - obj.start_at
            total_seconds = int(duration.total_seconds())
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60
            seconds = total_seconds % 60
            if hours > 0:
                return f'{hours}:{minutes:02d}:{seconds:02d}'
            return f'{minutes}:{seconds:02d}'
        return '-'
    duration_display.short_description = 'مدت زمان'
    
    def duration_calc(self, obj):
        """محاسبه مدت زمان در صفحه جزئیات"""
        return self.duration_display(obj)
    duration_calc.short_description = 'مدت زمان آزمون'


@admin.register(QuizResponse)
class QuizResponseAdmin(admin.ModelAdmin):
    list_display = ['id', 'quiz', 'question_preview', 'answer', 'score_display', 'done']
    list_filter = ['quiz', 'quiz__evaluation', 'done']
    search_fields = ['quiz__id', 'question__description', 'quiz__user__name']
    raw_id_fields = ['quiz', 'question']
    readonly_fields = ['id', 'score']
    ordering = ['quiz', 'id']
    
    def question_preview(self, obj):
        """پیش‌نمایش سوال"""
        if obj.question and obj.question.description:
            preview = obj.question.description[:40] + '...' if len(obj.question.description) > 40 else obj.question.description
            return format_html('<span title="{}">{}</span>', obj.question.description, preview)
        return '-'
    question_preview.short_description = 'سوال'
    
    def score_display(self, obj):
        """نمایش نمره با رنگ"""
        if obj.score is not None:
            color = 'green' if obj.score > 0 else 'red'
            return format_html(
                '<span style="color: {}; font-weight: bold;">{:.2f}</span>',
                color,
                obj.score
            )
        return '-'
    score_display.short_description = 'نمره'


@admin.register(QuizResponseEvaluation)
class QuizResponseEvaluationAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'quiz', 'evaluation_info', 'score_display', 'quiz_date']
    list_filter = ['user', 'quiz__evaluation', 'quiz__start_at']
    search_fields = ['user__name', 'user__mobile', 'quiz__id', 'quiz__evaluation__title']
    raw_id_fields = ['user', 'quiz']
    readonly_fields = ['id', 'score']
    ordering = ['-quiz__start_at', '-id']
    
    def evaluation_info(self, obj):
        """اطلاعات ارزیابی"""
        if obj.quiz and obj.quiz.evaluation:
            eval_obj = obj.quiz.evaluation
            return format_html(
                '<strong>{}</strong><br><small style="color: gray;">ID: {}</small>',
                eval_obj.title or f'Evaluation {eval_obj.id}',
                eval_obj.id
            )
        return '-'
    evaluation_info.short_description = 'ارزیابی'
    
    def score_display(self, obj):
        """نمایش نمره با رنگ و درصد"""
        if obj.score is not None:
            color = 'green' if obj.score >= 50 else 'orange' if obj.score >= 0 else 'red'
            return format_html(
                '<span style="color: {}; font-weight: bold; font-size: 14px;">{:.2f}%</span>',
                color,
                obj.score
            )
        return '-'
    score_display.short_description = 'نمره (%)'
    
    def quiz_date(self, obj):
        """تاریخ آزمون"""
        if obj.quiz and obj.quiz.start_at:
            return obj.quiz.start_at.strftime('%Y-%m-%d %H:%M')
        return '-'
    quiz_date.short_description = 'تاریخ آزمون'
