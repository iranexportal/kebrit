from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from django.db import transaction
from django.db.models import Q
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator
import random
from .models import Evaluation, Question, Quiz, QuizResponse, QuizResponseEvaluation
from .serializers import (
    EvaluationSerializer, QuestionSerializer, QuizSerializer,
    QuizResponseSerializer, QuizResponseEvaluationSerializer,
    QuestionForQuizSerializer, QuizSubmitSerializer, QuizResultSerializer
)
from users_app.permissions import CompanyPermission


@method_decorator(ratelimit(key='ip', rate='100/h', method='GET'), name='list')
@method_decorator(ratelimit(key='ip', rate='50/h', method='POST'), name='create')
@method_decorator(ratelimit(key='ip', rate='100/h', method='GET'), name='retrieve')
@method_decorator(ratelimit(key='ip', rate='50/h', method='PUT'), name='update')
@method_decorator(ratelimit(key='ip', rate='50/h', method='PATCH'), name='partial_update')
@method_decorator(ratelimit(key='ip', rate='50/h', method='DELETE'), name='destroy')
class EvaluationViewSet(viewsets.ModelViewSet):
    queryset = Evaluation.objects.select_related('mission', 'mission__company', 'user', 'user__company').all()
    serializer_class = EvaluationSerializer
    permission_classes = [CompanyPermission]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        if hasattr(self.request.user, 'company_id'):
            user_roles = self.request.user.user_roles.all()
            is_admin = any(ur.role.title.lower() == 'admin' for ur in user_roles)
            if not is_admin:
                queryset = queryset.filter(user__company_id=self.request.user.company_id)
        return queryset
    
    @action(detail=True, methods=['get'], url_path='questions')
    @method_decorator(ratelimit(key='ip', rate='100/h', method='GET'))
    def get_questions(self, request, pk=None):
        """
        دریافت تمام سوالات مربوط به یک Evaluation
        
        این endpoint تمام سوالات موجود در بانک سوالات یک Evaluation را برمی‌گرداند.
        شامل پاسخ صحیح (correct) است و برای مدرسان طراحی شده است.
        
        URL: GET /api/evaluations/{id}/questions/
        """
        try:
            evaluation = self.get_object()
        except Evaluation.DoesNotExist:
            return Response(
                {'error': 'Evaluation یافت نشد'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # دریافت تمام سوالات مربوط به این Evaluation
        questions = Question.objects.filter(evaluation=evaluation).order_by('id')
        
        # استفاده از QuestionSerializer که شامل تمام فیلدها از جمله correct است
        serializer = QuestionSerializer(questions, many=True)
        
        return Response({
            'evaluation_id': evaluation.id,
            'evaluation_details': EvaluationSerializer(evaluation).data,
            'total_questions': questions.count(),
            'questions': serializer.data
        }, status=status.HTTP_200_OK)


@method_decorator(ratelimit(key='ip', rate='100/h', method='GET'), name='list')
@method_decorator(ratelimit(key='ip', rate='50/h', method='POST'), name='create')
@method_decorator(ratelimit(key='ip', rate='100/h', method='GET'), name='retrieve')
@method_decorator(ratelimit(key='ip', rate='50/h', method='PUT'), name='update')
@method_decorator(ratelimit(key='ip', rate='50/h', method='PATCH'), name='partial_update')
@method_decorator(ratelimit(key='ip', rate='50/h', method='DELETE'), name='destroy')
class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.select_related('evaluation', 'evaluation__user', 'evaluation__user__company').all()
    serializer_class = QuestionSerializer
    permission_classes = [CompanyPermission]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        if hasattr(self.request.user, 'company_id'):
            user_roles = self.request.user.user_roles.all()
            is_admin = any(ur.role.title.lower() == 'admin' for ur in user_roles)
            if not is_admin:
                queryset = queryset.filter(evaluation__user__company_id=self.request.user.company_id)
        return queryset


@method_decorator(ratelimit(key='ip', rate='100/h', method='GET'), name='list')
@method_decorator(ratelimit(key='ip', rate='50/h', method='POST'), name='create')
@method_decorator(ratelimit(key='ip', rate='100/h', method='GET'), name='retrieve')
@method_decorator(ratelimit(key='ip', rate='50/h', method='PUT'), name='update')
@method_decorator(ratelimit(key='ip', rate='50/h', method='PATCH'), name='partial_update')
@method_decorator(ratelimit(key='ip', rate='50/h', method='DELETE'), name='destroy')
class QuizViewSet(viewsets.ModelViewSet):
    queryset = Quiz.objects.select_related('evaluation', 'evaluation__user', 'evaluation__user__company', 'user', 'user__company').all()
    serializer_class = QuizSerializer
    permission_classes = [CompanyPermission]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        if hasattr(self.request.user, 'company_id'):
            user_roles = self.request.user.user_roles.all()
            is_admin = any(ur.role.title.lower() == 'admin' for ur in user_roles)
            if not is_admin:
                queryset = queryset.filter(user__company_id=self.request.user.company_id)
        return queryset
    
    @action(detail=False, methods=['post'], url_path='start')
    @method_decorator(ratelimit(key='ip', rate='20/h', method='POST'))
    def start_quiz(self, request):
        """
        شروع یک کوئیز جدید برای دانشجو
        
        این endpoint یک کوئیز جدید می‌سازد و به تعداد number_of_question
        از سوالات evaluation به صورت تصادفی انتخاب می‌کند.
        
        Body:
        {
            "evaluation_id": 1
        }
        """
        evaluation_id = request.data.get('evaluation_id')
        
        if not evaluation_id:
            return Response(
                {'error': 'evaluation_id الزامی است'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            evaluation = Evaluation.objects.get(id=evaluation_id, is_active=True)
        except Evaluation.DoesNotExist:
            return Response(
                {'error': 'Evaluation یافت نشد یا غیرفعال است'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # بررسی دسترسی کاربر
        if hasattr(request.user, 'company_id'):
            user_roles = request.user.user_roles.all()
            is_admin = any(ur.role.title.lower() == 'admin' for ur in user_roles)
            if not is_admin:
                if evaluation.user and evaluation.user.company_id != request.user.company_id:
                    return Response(
                        {'error': 'دسترسی به این evaluation ندارید'},
                        status=status.HTTP_403_FORBIDDEN
                    )
        
        # بررسی اینکه آیا کوئیز فعال دیگری برای این کاربر و evaluation وجود دارد
        active_quiz = Quiz.objects.filter(
            evaluation=evaluation,
            user=request.user,
            state__in=['started', 'in_progress', None]
        ).exclude(end_at__isnull=False).first()
        
        if active_quiz:
            return Response(
                {
                    'error': 'یک کوئیز فعال برای این evaluation دارید',
                    'quiz_id': active_quiz.id
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # دریافت سوالات مربوط به این evaluation
        available_questions = Question.objects.filter(evaluation=evaluation)
        
        if not available_questions.exists():
            return Response(
                {'error': 'هیچ سوالی برای این evaluation وجود ندارد'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        number_of_questions = evaluation.number_of_question
        
        if available_questions.count() < number_of_questions:
            return Response(
                {
                    'error': f'تعداد سوالات موجود ({available_questions.count()}) کمتر از تعداد مورد نیاز ({number_of_questions}) است'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # انتخاب تصادفی سوالات
        selected_questions = random.sample(
            list(available_questions.values_list('id', flat=True)),
            number_of_questions
        )
        
        try:
            with transaction.atomic():
                # ایجاد کوئیز
                quiz = Quiz.objects.create(
                    evaluation=evaluation,
                    user=request.user,
                    state='started'
                )
                
                # ایجاد رکوردهای QuizResponse برای هر سوال (بدون پاسخ)
                quiz_responses = []
                for question_id in selected_questions:
                    question = Question.objects.get(id=question_id)
                    quiz_response = QuizResponse.objects.create(
                        quiz=quiz,
                        question=question,
                        answer=None,
                        score=None
                    )
                    quiz_responses.append(quiz_response)
                
                # بازگرداندن کوئیز با سوالات
                serializer = self.get_serializer(quiz)
                questions_data = QuestionForQuizSerializer(
                    Question.objects.filter(id__in=selected_questions),
                    many=True
                ).data
                
                return Response({
                    'quiz': serializer.data,
                    'questions': questions_data,
                    'message': 'کوئیز با موفقیت ایجاد شد'
                }, status=status.HTTP_201_CREATED)
                
        except Exception as e:
            return Response(
                {'error': f'خطا در ایجاد کوئیز: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['post'], url_path='submit')
    @method_decorator(ratelimit(key='ip', rate='20/h', method='POST'))
    def submit_quiz(self, request):
        """
        ارسال پاسخ‌های کوئیز و محاسبه نمره
        
        این endpoint پاسخ‌های دانشجو را دریافت می‌کند، نمره هر سوال را محاسبه می‌کند
        و نمره نهایی را در QuizResponseEvaluation ذخیره می‌کند.
        
        Body:
        {
            "quiz_id": 1,
            "responses": [
                {
                    "question_id": 1,
                    "answer": 2,
                    "done": "completed"
                },
                ...
            ]
        }
        """
        serializer = QuizSubmitSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {'error': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        quiz_id = serializer.validated_data['quiz_id']
        responses_data = serializer.validated_data['responses']
        
        try:
            quiz = Quiz.objects.select_related('evaluation', 'user').get(id=quiz_id)
        except Quiz.DoesNotExist:
            return Response(
                {'error': 'کوئیز یافت نشد'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # بررسی دسترسی
        if quiz.user_id != request.user.id:
            return Response(
                {'error': 'شما دسترسی به این کوئیز ندارید'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # بررسی اینکه کوئیز قبلاً تمام نشده باشد
        if quiz.end_at is not None:
            return Response(
                {'error': 'این کوئیز قبلاً تمام شده است'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # بررسی اینکه تمام سوالات کوئیز پاسخ داده شده باشند
        quiz_questions = Question.objects.filter(
            quiz_responses__quiz=quiz
        ).distinct()
        
        if len(responses_data) != quiz_questions.count():
            return Response(
                {
                    'error': f'تعداد پاسخ‌های ارسالی ({len(responses_data)}) با تعداد سوالات ({quiz_questions.count()}) مطابقت ندارد'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            with transaction.atomic():
                total_score = 0.0
                correct_count = 0
                wrong_count = 0
                
                # پردازش هر پاسخ
                for response_data in responses_data:
                    question_id = response_data['question_id']
                    student_answer = response_data.get('answer')
                    done = response_data.get('done', 'completed')
                    
                    try:
                        question = Question.objects.get(id=question_id, evaluation=quiz.evaluation)
                    except Question.DoesNotExist:
                        continue
                    
                    # پیدا کردن QuizResponse مربوطه
                    quiz_response = QuizResponse.objects.filter(
                        quiz=quiz,
                        question=question
                    ).first()
                    
                    if not quiz_response:
                        continue
                    
                    # محاسبه نمره
                    is_correct = False
                    score = 0.0
                    
                    if student_answer is not None and question.correct is not None:
                        if student_answer == question.correct:
                            is_correct = True
                            correct_count += 1
                            # استفاده از weight اگر وجود داشته باشد، در غیر این صورت 1
                            score = question.weight if question.weight else 1.0
                        else:
                            wrong_count += 1
                    
                    # به‌روزرسانی QuizResponse
                    quiz_response.answer = student_answer
                    quiz_response.score = score
                    quiz_response.done = done
                    quiz_response.save()
                    
                    total_score += score
                
                # محاسبه درصد
                total_questions = quiz_questions.count()
                percentage = (correct_count / total_questions * 100) if total_questions > 0 else 0
                
                # بررسی قبولی
                is_accept = total_score >= quiz.evaluation.accept_score if quiz.evaluation.accept_score else False
                
                # به‌روزرسانی کوئیز
                quiz.end_at = timezone.now()
                quiz.score = total_score
                quiz.is_accept = is_accept
                quiz.state = 'completed'
                quiz.save()
                
                # ایجاد QuizResponseEvaluation برای هر پاسخ (طبق ساختار فعلی مدل)
                # یا می‌توانیم یک رکورد برای کل کوئیز ایجاد کنیم
                # با توجه به ساختار فعلی، برای هر QuizResponse یک QuizResponseEvaluation ایجاد می‌کنیم
                quiz_responses = QuizResponse.objects.filter(quiz=quiz)
                for qr in quiz_responses:
                    QuizResponseEvaluation.objects.update_or_create(
                        user=request.user,
                        quiz_response=qr,
                        defaults={'score': qr.score or 0.0}
                    )
                
                # آماده‌سازی نتیجه
                result_data = {
                    'quiz_id': quiz.id,
                    'total_questions': total_questions,
                    'correct_answers': correct_count,
                    'wrong_answers': wrong_count,
                    'percentage': round(percentage, 2),
                    'total_score': round(total_score, 2),
                    'is_accept': is_accept,
                    'accept_score': quiz.evaluation.accept_score,
                    'responses': QuizResponseSerializer(quiz_responses, many=True).data
                }
                
                return Response({
                    'message': 'پاسخ‌های کوئیز با موفقیت ثبت شد',
                    'result': result_data
                }, status=status.HTTP_200_OK)
                
        except Exception as e:
            return Response(
                {'error': f'خطا در ثبت پاسخ‌ها: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=True, methods=['get'], url_path='questions')
    @method_decorator(ratelimit(key='ip', rate='100/h', method='GET'))
    def get_questions(self, request, pk=None):
        """
        دریافت سوالات یک کوئیز فعال
        """
        try:
            quiz = Quiz.objects.select_related('evaluation', 'user').prefetch_related(
                'responses', 'responses__question'
            ).get(id=pk)
        except Quiz.DoesNotExist:
            return Response(
                {'error': 'کوئیز یافت نشد'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # بررسی دسترسی
        if quiz.user_id != request.user.id:
            if hasattr(request.user, 'company_id'):
                user_roles = request.user.user_roles.all()
                is_admin = any(ur.role.title.lower() == 'admin' for ur in user_roles)
                if not is_admin:
                    return Response(
                        {'error': 'دسترسی به این کوئیز ندارید'},
                        status=status.HTTP_403_FORBIDDEN
                    )
        
        # دریافت سوالات کوئیز
        questions = Question.objects.filter(
            quiz_responses__quiz=quiz
        ).distinct()
        
        questions_data = QuestionForQuizSerializer(questions, many=True).data
        
        # دریافت پاسخ‌های فعلی (اگر وجود داشته باشند)
        responses = quiz.responses.all()
        responses_dict = {r.question_id: {'answer': r.answer, 'done': r.done} for r in responses}
        
        # اضافه کردن وضعیت پاسخ به هر سوال
        for question_data in questions_data:
            question_id = question_data['id']
            if question_id in responses_dict:
                question_data['current_answer'] = responses_dict[question_id]['answer']
                question_data['done'] = responses_dict[question_id]['done']
            else:
                question_data['current_answer'] = None
                question_data['done'] = None
        
        return Response({
            'quiz_id': quiz.id,
            'evaluation_id': quiz.evaluation_id,
            'start_at': quiz.start_at,
            'end_at': quiz.end_at,
            'state': quiz.state,
            'questions': questions_data
        }, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['get'], url_path='result')
    @method_decorator(ratelimit(key='ip', rate='100/h', method='GET'))
    def get_result(self, request, pk=None):
        """
        دریافت نتیجه نهایی کوئیز
        """
        try:
            quiz = Quiz.objects.select_related('evaluation', 'user').prefetch_related(
                'responses', 'responses__question'
            ).get(id=pk)
        except Quiz.DoesNotExist:
            return Response(
                {'error': 'کوئیز یافت نشد'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # بررسی دسترسی
        if hasattr(request.user, 'company_id'):
            user_roles = request.user.user_roles.all()
            is_admin = any(ur.role.title.lower() == 'admin' for ur in user_roles)
            if not is_admin:
                if quiz.user_id != request.user.id and quiz.user.company_id != request.user.company_id:
                    return Response(
                        {'error': 'دسترسی به این کوئیز ندارید'},
                        status=status.HTTP_403_FORBIDDEN
                    )
        
        if quiz.end_at is None:
            return Response(
                {'error': 'این کوئیز هنوز تمام نشده است'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # محاسبه آمار
        responses = quiz.responses.all()
        total_questions = responses.count()
        correct_count = sum(1 for r in responses if r.score and r.score > 0)
        wrong_count = total_questions - correct_count
        total_score = sum(r.score or 0.0 for r in responses)
        percentage = (correct_count / total_questions * 100) if total_questions > 0 else 0
        
        result_data = {
            'quiz_id': quiz.id,
            'total_questions': total_questions,
            'correct_answers': correct_count,
            'wrong_answers': wrong_count,
            'percentage': round(percentage, 2),
            'total_score': round(total_score, 2),
            'is_accept': quiz.is_accept,
            'accept_score': quiz.evaluation.accept_score,
            'start_at': quiz.start_at,
            'end_at': quiz.end_at,
            'responses': QuizResponseSerializer(responses, many=True).data
        }
        
        return Response(result_data, status=status.HTTP_200_OK)


@method_decorator(ratelimit(key='ip', rate='100/h', method='GET'), name='list')
@method_decorator(ratelimit(key='ip', rate='50/h', method='POST'), name='create')
@method_decorator(ratelimit(key='ip', rate='100/h', method='GET'), name='retrieve')
@method_decorator(ratelimit(key='ip', rate='50/h', method='PUT'), name='update')
@method_decorator(ratelimit(key='ip', rate='50/h', method='PATCH'), name='partial_update')
@method_decorator(ratelimit(key='ip', rate='50/h', method='DELETE'), name='destroy')
class QuizResponseViewSet(viewsets.ModelViewSet):
    queryset = QuizResponse.objects.select_related('quiz', 'quiz__user', 'quiz__user__company', 'question').all()
    serializer_class = QuizResponseSerializer
    permission_classes = [CompanyPermission]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        if hasattr(self.request.user, 'company_id'):
            user_roles = self.request.user.user_roles.all()
            is_admin = any(ur.role.title.lower() == 'admin' for ur in user_roles)
            if not is_admin:
                queryset = queryset.filter(quiz__user__company_id=self.request.user.company_id)
        return queryset


@method_decorator(ratelimit(key='ip', rate='100/h', method='GET'), name='list')
@method_decorator(ratelimit(key='ip', rate='50/h', method='POST'), name='create')
@method_decorator(ratelimit(key='ip', rate='100/h', method='GET'), name='retrieve')
@method_decorator(ratelimit(key='ip', rate='50/h', method='PUT'), name='update')
@method_decorator(ratelimit(key='ip', rate='50/h', method='PATCH'), name='partial_update')
@method_decorator(ratelimit(key='ip', rate='50/h', method='DELETE'), name='destroy')
class QuizResponseEvaluationViewSet(viewsets.ModelViewSet):
    queryset = QuizResponseEvaluation.objects.select_related('user', 'user__company', 'quiz_response', 'quiz_response__quiz', 'quiz_response__quiz__user').all()
    serializer_class = QuizResponseEvaluationSerializer
    permission_classes = [CompanyPermission]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        if hasattr(self.request.user, 'company_id'):
            user_roles = self.request.user.user_roles.all()
            is_admin = any(ur.role.title.lower() == 'admin' for ur in user_roles)
            if not is_admin:
                queryset = queryset.filter(user__company_id=self.request.user.company_id)
        return queryset
