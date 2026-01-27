from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action, api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from django.utils import timezone
from django.db import transaction
from django.db.models import Q
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator
import random
from .models import EvaluationType, Evaluation, Question, Quiz, QuizResponse, QuizResponseEvaluation
from .serializers import (
    EvaluationTypeSerializer, EvaluationSerializer, QuestionSerializer, QuizSerializer,
    QuizResponseSerializer, QuizResponseEvaluationSerializer,
    QuestionForQuizSerializer, QuizSubmitSerializer, QuizResultSerializer
)
from .student_report_serializers import (
    MissionReportRequestSerializer,
    MissionReportSerializer,
    MissionAttemptSerializer,
)
from users_app.permissions import CompanyPermission
from kebrit_api.authentication_client import ClientTokenAuthentication
from kebrit_api.permissions import IsClientTokenAuthenticated
from users_app.models import User
from roadmap_app.models import Mission


@method_decorator(ratelimit(key='ip', rate='100/h', method='GET'), name='list')
@method_decorator(ratelimit(key='ip', rate='50/h', method='POST'), name='create')
@method_decorator(ratelimit(key='ip', rate='100/h', method='GET'), name='retrieve')
@method_decorator(ratelimit(key='ip', rate='50/h', method='PUT'), name='update')
@method_decorator(ratelimit(key='ip', rate='50/h', method='PATCH'), name='partial_update')
@method_decorator(ratelimit(key='ip', rate='50/h', method='DELETE'), name='destroy')
class EvaluationTypeViewSet(viewsets.ModelViewSet):
    queryset = EvaluationType.objects.all()
    serializer_class = EvaluationTypeSerializer
    permission_classes = [CompanyPermission]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        # مرتب‌سازی بر اساس id
        queryset = queryset.order_by('id')
        return queryset


@method_decorator(ratelimit(key='ip', rate='100/h', method='GET'), name='list')
@method_decorator(ratelimit(key='ip', rate='50/h', method='POST'), name='create')
@method_decorator(ratelimit(key='ip', rate='100/h', method='GET'), name='retrieve')
@method_decorator(ratelimit(key='ip', rate='50/h', method='PUT'), name='update')
@method_decorator(ratelimit(key='ip', rate='50/h', method='PATCH'), name='partial_update')
@method_decorator(ratelimit(key='ip', rate='50/h', method='DELETE'), name='destroy')
class EvaluationViewSet(viewsets.ModelViewSet):
    queryset = Evaluation.objects.select_related('type', 'mission', 'mission__company', 'user', 'user__company').all()
    serializer_class = EvaluationSerializer
    permission_classes = [CompanyPermission]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        # فیلتر فقط بر اساس شرکت توکن مشتری
        if hasattr(self.request, 'auth_company') and self.request.auth_company:
            queryset = queryset.filter(user__company_id=self.request.auth_company.id)
        # مرتب‌سازی برای جلوگیری از warning pagination
        queryset = queryset.order_by('-create_at', '-id')
        return queryset
    
    def get_serializer_context(self):
        """اضافه کردن request به context برای دسترسی به کاربر در serializer"""
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
    
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
            'evaluation_details': EvaluationSerializer(evaluation, context={'request': request}).data,
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
        if hasattr(self.request, 'auth_company') and self.request.auth_company:
            queryset = queryset.filter(evaluation__user__company_id=self.request.auth_company.id)
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
    authentication_classes = [ClientTokenAuthentication]
    permission_classes = [CompanyPermission]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        if hasattr(self.request, 'auth_company') and self.request.auth_company:
            queryset = queryset.filter(user__company_id=self.request.auth_company.id)
        # مرتب‌سازی به ترتیب جدیدترین به قدیمی‌ترین بر اساس start_at
        queryset = queryset.order_by('-start_at')
        return queryset
    
    @action(detail=False, methods=['post'], url_path='start')
    @method_decorator(ratelimit(key='ip', rate='20/h', method='POST'))
    def start_quiz(self, request):
        """
        شروع یک کوئیز جدید یا بازگرداندن کوئیز فعال
        
        این endpoint ابتدا بررسی می‌کند که آیا کوئیز فعالی برای این کاربر و evaluation
        وجود دارد یا نه. اگر وجود داشته باشد، همان کوئیز فعال را با سوالات و پاسخ‌های
        فعلی برمی‌گرداند. در غیر این صورت، یک کوئیز جدید می‌سازد و به تعداد
        number_of_question از سوالات evaluation به صورت تصادفی انتخاب می‌کند.
        
        Body:
        {
            "evaluation_id": 1
        }
        
        Response (اگر کوئیز فعال وجود داشته باشد):
        {
            "quiz": {...},
            "questions": [...],
            "message": "کوئیز فعال شما بازگردانده شد",
            "is_existing": true
        }
        
        Response (اگر کوئیز جدید ایجاد شود):
        {
            "quiz": {...},
            "questions": [...],
            "message": "کوئیز با موفقیت ایجاد شد",
            "is_existing": false
        }
        """
        evaluation_id = request.data.get('evaluation_id')
        
        if not evaluation_id:
            return Response(
                {'error': 'evaluation_id الزامی است'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            evaluation = Evaluation.objects.select_related('type', 'mission', 'user').get(id=evaluation_id, is_active=True)
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
        ).exclude(end_at__isnull=False).prefetch_related('responses', 'responses__question').first()
        
        # اگر کوئیز فعال وجود دارد، همان را برمی‌گردانیم
        if active_quiz:
            # دریافت سوالات کوئیز فعال
            quiz_questions = Question.objects.filter(
                quiz_responses__quiz=active_quiz
            ).distinct()
            
            # دریافت پاسخ‌های فعلی کاربر
            responses = active_quiz.responses.all()
            responses_dict = {r.question_id: {'answer': r.answer, 'done': r.done} for r in responses}
            
            # آماده‌سازی سوالات با پاسخ‌های فعلی
            questions_data = QuestionForQuizSerializer(quiz_questions, many=True).data
            for question_data in questions_data:
                question_id = question_data['id']
                if question_id in responses_dict:
                    question_data['current_answer'] = responses_dict[question_id]['answer']
                    question_data['done'] = responses_dict[question_id]['done']
                else:
                    question_data['current_answer'] = None
                    question_data['done'] = None
            
            # بازگرداندن کوئیز فعال
            serializer = self.get_serializer(active_quiz)
            return Response({
                'quiz': serializer.data,
                'questions': questions_data,
                'message': 'کوئیز فعال شما بازگردانده شد',
                'is_existing': True
            }, status=status.HTTP_200_OK)
        
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
                    'message': 'کوئیز با موفقیت ایجاد شد',
                    'is_existing': False
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
        و درصد نمره (percentage) را در QuizResponseEvaluation به عنوان کارنامه کلی آزمون ذخیره می‌کند.
        
        برای سوالات چندگزینه‌ای (question.type = true):
        - answer باید یک عدد (integer) باشد که شماره گزینه را نشان می‌دهد
        - نمره به صورت خودکار محاسبه می‌شود (مقایسه با question.correct)
        
        برای سوالات تشریحی (question.type = false):
        - answer باید یک متن (string) باشد که پاسخ تشریحی کاربر است
        - نمره به صورت خودکار 0 تنظیم می‌شود (باید بعداً توسط مدرس تعیین شود)
        - فقط سوالات چندگزینه‌ای در محاسبه درصد در نظر گرفته می‌شوند
        
        Body:
        {
            "quiz_id": 1,
            "responses": [
                {
                    "question_id": 1,
                    "answer": 2,  // برای چندگزینه‌ای: عدد (1-4)
                    "done": "completed"
                },
                {
                    "question_id": 2,
                    "answer": "پاسخ تشریحی کاربر...",  // برای تشریحی: متن
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
        
        # بررسی دسترسی به آزمون شرکت
        if hasattr(request.user, 'company_id'):
            user_roles = request.user.user_roles.all()
            is_admin = any(ur.role.title.lower() == 'admin' for ur in user_roles)
            if not is_admin:
                # بررسی اینکه evaluation متعلق به همان شرکت باشد
                if quiz.evaluation.user and quiz.evaluation.user.company_id != request.user.company_id:
                    return Response(
                        {'error': 'شما دسترسی به آزمون این شرکت ندارید'},
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
                multiple_choice_count = 0  # تعداد سوالات چندگزینه‌ای
                
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
                    
                    # اگر QuizResponse وجود نداشته باشد، آن را ایجاد می‌کنیم
                    if not quiz_response:
                        quiz_response = QuizResponse.objects.create(
                            quiz=quiz,
                            question=question,
                            answer=None,
                            score=None,
                            done=None
                        )
                    
                    # محاسبه نمره بر اساس نوع سوال
                    is_correct = False
                    score = 0.0
                    
                    if question.type:  # سوال چندگزینه‌ای (type = True)
                        multiple_choice_count += 1
                        # تبدیل answer به integer برای مقایسه
                        try:
                            student_answer_int = int(student_answer) if student_answer is not None and student_answer != '' else None
                        except (ValueError, TypeError):
                            student_answer_int = None
                        
                        if student_answer_int is not None and question.correct is not None:
                            if student_answer_int == question.correct:
                                is_correct = True
                                correct_count += 1
                                # استفاده از weight اگر وجود داشته باشد، در غیر این صورت 1
                                score = question.weight if question.weight else 1.0
                            else:
                                wrong_count += 1
                        
                        # ذخیره answer به صورت string (برای سازگاری)
                        quiz_response.answer = str(student_answer_int) if student_answer_int is not None else None
                    else:  # سوال تشریحی (type = False)
                        # برای سوالات تشریحی، answer به صورت text ذخیره می‌شود
                        # نمره به صورت دستی توسط مدرس داده می‌شود، پس فعلاً 0 می‌گذاریم
                        quiz_response.answer = student_answer if student_answer else None
                        score = 0.0  # نمره باید بعداً توسط مدرس تعیین شود
                        # برای سوالات تشریحی، correct_count و wrong_count را افزایش نمی‌دهیم
                    
                    # به‌روزرسانی QuizResponse
                    quiz_response.score = score
                    quiz_response.done = done
                    quiz_response.save()
                    
                    total_score += score
                
                # محاسبه درصد (فقط برای سوالات چندگزینه‌ای)
                # اگر سوالات تشریحی وجود داشته باشند، فقط سوالات چندگزینه‌ای در محاسبه درصد در نظر گرفته می‌شوند
                percentage = (correct_count / multiple_choice_count * 100) if multiple_choice_count > 0 else 0
                
                # تعداد کل سوالات
                total_questions = quiz_questions.count()
                
                # بررسی قبولی
                is_accept = percentage >= quiz.evaluation.accept_score if quiz.evaluation.accept_score else False
                
                # به‌روزرسانی کوئیز
                quiz.end_at = timezone.now()
                quiz.score = total_score
                quiz.is_accept = is_accept
                print(quiz.evaluation.type.id)
                if (quiz.evaluation.type.id == 1 or quiz.evaluation.type.id == 3):
                    quiz.state = 'completed'
                elif (quiz.evaluation.type.id == 2 or quiz.evaluation.type.id == 4):
                    quiz.state = 'pending'
                quiz.save()
                
                # ایجاد QuizResponseEvaluation برای کل کوئیز (کارنامه کلی آزمون)
                # score در اینجا percentage است
                QuizResponseEvaluation.objects.update_or_create(
                    user=request.user,
                    quiz=quiz,
                    defaults={'score': round(percentage, 2)}
                )
                
                # اگر کاربر در آزمون قبول شده باشد، MissionResult را ثبت می‌کنیم
                if is_accept and quiz.evaluation.mission:
                    from roadmap_app.models import MissionResult
                    MissionResult.objects.update_or_create(
                        mission=quiz.evaluation.mission,
                        user=request.user,
                        quiz_id=quiz.id,
                        defaults={
                            'state': 'completed',
                            'user_grant': None,
                        }
                    )
                
                # دریافت تمام پاسخ‌های به‌روزرسانی شده
                quiz_responses = QuizResponse.objects.filter(quiz=quiz).select_related('question')
                
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
    
    @action(detail=True, methods=['get'], url_path='questions', authentication_classes=[], permission_classes=[permissions.AllowAny])
    @method_decorator(ratelimit(key='ip', rate='100/h', method='GET'))
    def get_questions(self, request, pk=None):
        """
        دریافت سوالات یک کوئیز فعال
        """
        # #region agent log
        import json
        try:
            with open('/Users/hajrezvan/Desktop/Projects/Kebrit/api/.cursor/debug.log', 'a') as f:
                log_entry = json.dumps({
                    "sessionId": "debug-session",
                    "runId": "run1",
                    "hypothesisId": "D",
                    "location": "views.py:547",
                    "message": "get_questions called",
                    "data": {
                        "quiz_id": pk,
                        "has_launch_id": bool(request.GET.get('launch_id')),
                        "launch_id": request.GET.get('launch_id'),
                        "has_token_query": bool(request.GET.get('token')),
                        "has_auth_header": bool(request.META.get('HTTP_AUTHORIZATION')),
                        "auth_header_preview": request.META.get('HTTP_AUTHORIZATION', '')[:50] if request.META.get('HTTP_AUTHORIZATION') else None,
                        "has_user": hasattr(request, 'user'),
                        "user_type": type(request.user).__name__ if hasattr(request, 'user') else None,
                        "user_id": getattr(request.user, 'id', None) if hasattr(request, 'user') else None,
                        "user_has_id_attr": hasattr(request.user, 'id') if hasattr(request, 'user') else False,
                        "is_authenticated": getattr(request.user, 'is_authenticated', False) if hasattr(request, 'user') else False,
                        "has_auth_company": hasattr(request, 'auth_company') and bool(request.auth_company),
                        "request_auth": str(type(request.auth)) if hasattr(request, 'auth') else None
                    },
                    "timestamp": int(__import__('time').time() * 1000)
                }) + "\n"
                f.write(log_entry)
        except Exception:
            pass
        # #endregion
        
        try:
            quiz = Quiz.objects.select_related('evaluation', 'user', 'user__company').prefetch_related(
                'responses', 'responses__question'
            ).get(id=pk)
        except Quiz.DoesNotExist:
            return Response(
                {'error': 'کوئیز یافت نشد'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # اگر launch_id در query parameter باشد، بررسی دسترسی از طریق ExamLaunch
        launch_id = request.GET.get('launch_id')
        if launch_id:
            try:
                from kebrit_api.models import ExamLaunch
                launch = ExamLaunch.objects.get(uuid=launch_id, quiz_id=quiz.id)
                # اگر launch پیدا شد و متعلق به این quiz است، اجازه دسترسی بده
                # #region agent log
                try:
                    with open('/Users/hajrezvan/Desktop/Projects/Kebrit/api/.cursor/debug.log', 'a') as f:
                        log_entry = json.dumps({
                            "sessionId": "debug-session",
                            "runId": "run1",
                            "hypothesisId": "D",
                            "location": "views.py:594",
                            "message": "Launch-based access granted",
                            "data": {
                                "launch_id": str(launch_id),
                                "quiz_id": quiz.id,
                                "launch_quiz_id": launch.quiz_id
                            },
                            "timestamp": int(__import__('time').time() * 1000)
                        }) + "\n"
                        f.write(log_entry)
                except Exception:
                    pass
                # #endregion
                # اگر launch پیدا شد، نیازی به بررسی احراز هویت نیست - مستقیماً به ادامه برو
            except Exception as e:
                # #region agent log
                try:
                    with open('/Users/hajrezvan/Desktop/Projects/Kebrit/api/.cursor/debug.log', 'a') as f:
                        log_entry = json.dumps({
                            "sessionId": "debug-session",
                            "runId": "run1",
                            "hypothesisId": "D",
                            "location": "views.py:616",
                            "message": "Launch not found, checking auth",
                            "data": {
                                "launch_id": str(launch_id),
                                "quiz_id": quiz.id,
                                "error": str(e)
                            },
                            "timestamp": int(__import__('time').time() * 1000)
                        }) + "\n"
                        f.write(log_entry)
                except Exception:
                    pass
                # #endregion
                # اگر launch پیدا نشد، به بررسی‌های معمول برو
                # بررسی دسترسی - پشتیبانی از هر دو نوع احراز هویت (JWT و ClientToken)
                # اگر با ClientToken احراز هویت شده باشد
                if hasattr(request, 'auth_company') and request.auth_company:
                    # بررسی اینکه کوئیز متعلق به همان شرکت مشتری باشد
                    if quiz.user.company_id != request.auth_company.id:
                        return Response(
                            {'error': 'دسترسی به این کوئیز ندارید'},
                            status=status.HTTP_403_FORBIDDEN
                        )
                # اگر با JWT احراز هویت شده باشد
                elif hasattr(request.user, 'id'):
                    # بررسی دسترسی کاربر عادی
                    if quiz.user_id != request.user.id:
                        if hasattr(request.user, 'company_id'):
                            user_roles = request.user.user_roles.all()
                            is_admin = any(ur.role.title.lower() == 'admin' for ur in user_roles)
                            if not is_admin:
                                return Response(
                                    {'error': 'دسترسی به این کوئیز ندارید'},
                                    status=status.HTTP_403_FORBIDDEN
                                )
                else:
                    # اگر هیچ نوع احراز هویتی وجود نداشت
                    return Response(
                        {'error': 'احراز هویت لازم است'},
                        status=status.HTTP_401_UNAUTHORIZED
                    )
        else:
            # بررسی دسترسی - پشتیبانی از هر دو نوع احراز هویت (JWT و ClientToken)
            # اگر با ClientToken احراز هویت شده باشد
            if hasattr(request, 'auth_company') and request.auth_company:
                # بررسی اینکه کوئیز متعلق به همان شرکت مشتری باشد
                if quiz.user.company_id != request.auth_company.id:
                    return Response(
                        {'error': 'دسترسی به این کوئیز ندارید'},
                        status=status.HTTP_403_FORBIDDEN
                    )
            # اگر با JWT احراز هویت شده باشد
            elif hasattr(request.user, 'id'):
                # بررسی دسترسی کاربر عادی
                if quiz.user_id != request.user.id:
                    if hasattr(request.user, 'company_id'):
                        user_roles = request.user.user_roles.all()
                        is_admin = any(ur.role.title.lower() == 'admin' for ur in user_roles)
                        if not is_admin:
                            return Response(
                                {'error': 'دسترسی به این کوئیز ندارید'},
                                status=status.HTTP_403_FORBIDDEN
                            )
            else:
                # اگر هیچ نوع احراز هویتی وجود نداشت
                return Response(
                    {'error': 'احراز هویت لازم است'},
                    status=status.HTTP_401_UNAUTHORIZED
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
    
    @action(detail=True, methods=['get'], url_path='result', authentication_classes=[], permission_classes=[permissions.AllowAny])
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
        
        # اگر launch_id در query parameter باشد، بررسی دسترسی از طریق ExamLaunch
        launch_id = request.GET.get('launch_id')
        if launch_id:
            try:
                from kebrit_api.models import ExamLaunch
                launch = ExamLaunch.objects.get(uuid=launch_id, quiz_id=quiz.id)
                # اگر launch پیدا شد و متعلق به این quiz است، اجازه دسترسی بده
            except Exception:
                # اگر launch پیدا نشد، به بررسی‌های معمول برو
                pass
        else:
            # بررسی دسترسی - پشتیبانی از هر دو نوع احراز هویت (JWT و ClientToken)
            # اگر با ClientToken احراز هویت شده باشد
            if hasattr(request, 'auth_company') and request.auth_company:
                # بررسی اینکه کوئیز متعلق به همان شرکت مشتری باشد
                if quiz.user.company_id != request.auth_company.id:
                    return Response(
                        {'error': 'دسترسی به این کوئیز ندارید'},
                        status=status.HTTP_403_FORBIDDEN
                    )
            # اگر با JWT احراز هویت شده باشد
            elif hasattr(request.user, 'id'):
                # بررسی دسترسی کاربر عادی
                if quiz.user_id != request.user.id:
                    if hasattr(request.user, 'company_id'):
                        user_roles = request.user.user_roles.all()
                        is_admin = any(ur.role.title.lower() == 'admin' for ur in user_roles)
                        if not is_admin:
                            return Response(
                                {'error': 'دسترسی به این کوئیز ندارید'},
                                status=status.HTTP_403_FORBIDDEN
                            )
            else:
                # اگر هیچ نوع احراز هویتی وجود نداشت، بررسی کن که آیا quiz متعلق به یک launch است
                from kebrit_api.models import ExamLaunch
                launch = ExamLaunch.objects.filter(quiz_id=quiz.id, completed_at__isnull=False).order_by("-created_at").first()
                if not launch:
                    return Response(
                        {'error': 'احراز هویت لازم است'},
                        status=status.HTTP_401_UNAUTHORIZED
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
        if hasattr(self.request, 'auth_company') and self.request.auth_company:
            queryset = queryset.filter(quiz__user__company_id=self.request.auth_company.id)
        return queryset


@method_decorator(ratelimit(key='ip', rate='100/h', method='GET'), name='list')
@method_decorator(ratelimit(key='ip', rate='50/h', method='POST'), name='create')
@method_decorator(ratelimit(key='ip', rate='100/h', method='GET'), name='retrieve')
@method_decorator(ratelimit(key='ip', rate='50/h', method='PUT'), name='update')
@method_decorator(ratelimit(key='ip', rate='50/h', method='PATCH'), name='partial_update')
@method_decorator(ratelimit(key='ip', rate='50/h', method='DELETE'), name='destroy')
class QuizResponseEvaluationViewSet(viewsets.ModelViewSet):
    queryset = QuizResponseEvaluation.objects.select_related('user', 'user__company', 'quiz', 'quiz__evaluation', 'quiz__user').all()
    serializer_class = QuizResponseEvaluationSerializer
    permission_classes = [CompanyPermission]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        if hasattr(self.request, 'auth_company') and self.request.auth_company:
            queryset = queryset.filter(user__company_id=self.request.auth_company.id)
        return queryset


@api_view(['POST'])
@authentication_classes([ClientTokenAuthentication])
@permission_classes([IsClientTokenAuthenticated])
@method_decorator(ratelimit(key='ip', rate='50/h', method='POST'))
def mission_student_report(request):
    """
    دریافت کارنامه دانشجو در یک ماموریت مشخص بر اساس:
    - شماره موبایل دانشجو
    - شناسه ماموریت
    احراز هویت فقط با توکن مشتری (Client Token) انجام می‌شود.
    """
    req_serializer = MissionReportRequestSerializer(data=request.data)
    if not req_serializer.is_valid():
        return Response({'error': req_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    mobile = req_serializer.validated_data['mobile']
    mission_id = req_serializer.validated_data['mission_id']

    # شرکت از روی توکن مشتری تعیین می‌شود
    company = getattr(request, 'auth_company', None)
    if company is None:
        return Response({'error': 'توکن مشتری نامعتبر است'}, status=status.HTTP_401_UNAUTHORIZED)

    # پیدا کردن دانشجو در همان شرکت
    try:
        user = User.objects.get(mobile=mobile, company_id=company.id)
    except User.DoesNotExist:
        return Response({'error': 'دانشجو با این شماره موبایل در این شرکت یافت نشد'}, status=status.HTTP_404_NOT_FOUND)

    # پیدا کردن ماموریت متناسب با شرکت
    try:
        mission = Mission.objects.get(id=mission_id, company_id=company.id)
    except Mission.DoesNotExist:
        return Response({'error': 'ماموریت یافت نشد یا متعلق به این شرکت نیست'}, status=status.HTTP_404_NOT_FOUND)

    # پیدا کردن تمام evaluation های مرتبط با این ماموریت
    evaluations = Evaluation.objects.filter(mission=mission, is_active=True).order_by('id')

    if not evaluations.exists():
        empty_report = MissionReportSerializer({
            'mission_id': mission.id,
            'mobile': mobile,
            'user_id': user.id,
            'attempts': [],
        })
        return Response(empty_report.data, status=status.HTTP_200_OK)

    # همه کوئیزهای تمام‌شده دانشجو روی این ماموریت (ممکن است چند evaluation داشته باشد)
    quizzes = (
        Quiz.objects.filter(evaluation__in=evaluations, user=user, end_at__isnull=False)
        .select_related('evaluation')
        .order_by('start_at')
    )

    attempts = []
    for quiz in quizzes:
        qre = (
            QuizResponseEvaluation.objects.filter(user=user, quiz=quiz)
            .order_by('-id')
            .first()
        )
        percentage = qre.score if qre and qre.score is not None else None

        attempts.append({
            'evaluation_id': quiz.evaluation_id,
            'quiz_id': quiz.id,
            'percentage': round(percentage, 2) if percentage is not None else None,
            'total_score': round(quiz.score, 2) if quiz.score is not None else None,
            'is_accept': bool(quiz.is_accept) if quiz.is_accept is not None else None,
            'accept_score': quiz.evaluation.accept_score,
            'start_at': quiz.start_at,
            'end_at': quiz.end_at,
        })

    report = MissionReportSerializer({
        'mission_id': mission.id,
        'mobile': mobile,
        'user_id': user.id,
        'attempts': attempts,
    })

    return Response(report.data, status=status.HTTP_200_OK)
