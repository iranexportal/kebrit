import random
from urllib.parse import urlencode, urlparse, parse_qsl, urlunparse

from django.db import IntegrityError, transaction
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.conf import settings

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from kebrit_api.authentication_client import ClientTokenAuthentication
from kebrit_api.permissions import IsClientTokenAuthenticated
from kebrit_api.models import ExamLaunch

from users_app.models import User
from .models import Evaluation, Question, Quiz, QuizResponse, QuizResponseEvaluation
from .serializers import QuestionForQuizSerializer, QuizResponseSerializer
from .integration_serializers import ClientExamLaunchSerializer, LaunchAnswerSerializer, LaunchSubmitSerializer


def _build_callback_url(callback_url: str, params: dict) -> str:
    parsed = urlparse(callback_url)
    query = dict(parse_qsl(parsed.query, keep_blank_values=True))
    query.update({k: str(v) for k, v in params.items() if v is not None})
    return urlunparse(parsed._replace(query=urlencode(query, doseq=True)))


def _validate_callback_url(allowed_hosts: str | None, callback_url: str) -> str:
    """
    Validate callback URL format. All hosts are allowed.
    
    Args:
        allowed_hosts: (Deprecated - not used anymore, kept for backward compatibility)
        callback_url: The callback URL to validate
    
    Returns:
        Validated callback URL
    
    Raises:
        ValueError: If URL format is invalid
    """
    parsed = urlparse(callback_url)
    if parsed.scheme not in ("http", "https") or not parsed.netloc:
        raise ValueError("Invalid callback_url")

    # All hosts are allowed - no host restriction
    return callback_url


def _get_company_evaluation(company_id: int, eurl: int):
    return (
        Evaluation.objects.select_related("type", "mission", "mission__company", "user", "user__company")
        .filter(id=eurl, is_active=True)
        .filter(Q(user__company_id=company_id) | Q(mission__company_id=company_id))
        .first()
    )


class ClientExamInfoView(APIView):
    """
    Customer fetches exam info (by numeric eurl) to show it on their own site.
    """

    authentication_classes = [ClientTokenAuthentication]
    permission_classes = [IsClientTokenAuthenticated]

    def get(self, request, eurl: int):
        company = request.auth_company
        evaluation = _get_company_evaluation(company.id, eurl)
        if not evaluation:
            return Response({"error": "Evaluation یافت نشد"}, status=status.HTTP_404_NOT_FOUND)

        data = {
            "eurl": evaluation.id,
            "title": evaluation.title,
            "type": evaluation.type_id,
            "accept_score": evaluation.accept_score,
            "number_of_question": evaluation.number_of_question,
            "duration": evaluation.duration,
            "can_back": evaluation.can_back,
            "is_active": evaluation.is_active,
        }
        return Response(data, status=status.HTTP_200_OK)


class ClientExamLaunchView(APIView):
    """
    Customer starts an exam for a student:
    - authenticates by customer token header
    - creates/updates student record under that customer
    - creates (or resumes) a Quiz
    - returns a launch UUID for redirecting student to our exam frontend
    """

    authentication_classes = [ClientTokenAuthentication]
    permission_classes = [IsClientTokenAuthenticated]

    def post(self, request):
        serializer = ClientExamLaunchSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        company = request.auth_company
        client_token = request.auth_client_token

        student_uuid = serializer.validated_data["student_uuid"]
        mobile = serializer.validated_data["mobile"]
        eurl = serializer.validated_data["eurl"]
        callback_url = serializer.validated_data["callback_url"]
        name = serializer.validated_data.get("name", "")

        try:
            callback_url = _validate_callback_url(client_token.allowed_callback_hosts, callback_url)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        evaluation = _get_company_evaluation(company.id, eurl)
        if not evaluation:
            return Response({"error": "Evaluation یافت نشد یا متعلق به این مشتری نیست"}, status=status.HTTP_404_NOT_FOUND)

        # Upsert student (per company)
        student = User.objects.filter(company_id=company.id, uuid=student_uuid).first()
        try:
            if not student:
                student = User.objects.create(
                    company_id=company.id,
                    uuid=student_uuid,
                    mobile=mobile,
                    name=name,  # minimal placeholder
                )
            else:
                update_fields = []
                if mobile and student.mobile != mobile:
                    student.mobile = mobile
                    update_fields.append("mobile")
                if name and student.name != name:
                    student.name = name
                    update_fields.append("name")
                if update_fields:
                    student.save(update_fields=update_fields)
        except IntegrityError:
            return Response(
                {"error": "خطا در ایجاد دانشجو (احتمالاً migration های یکتایی mobile اعمال نشده‌اند)"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        # Resume active quiz if exists
        active_quiz = (
            Quiz.objects.filter(evaluation=evaluation, user=student, end_at__isnull=True)
            .filter(state__in=["started", "in_progress", None])
            .order_by("-start_at")
            .prefetch_related("responses", "responses__question")
            .first()
        )

        is_existing = bool(active_quiz)
        if active_quiz:
            quiz = active_quiz
        else:
            available_questions = Question.objects.filter(evaluation=evaluation)
            if not available_questions.exists():
                return Response({"error": "هیچ سوالی برای این آزمون وجود ندارد"}, status=status.HTTP_400_BAD_REQUEST)

            n = evaluation.number_of_question
            if available_questions.count() < n:
                return Response(
                    {"error": f"تعداد سوالات موجود کمتر از تعداد مورد نیاز است ({available_questions.count()} < {n})"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            selected_ids = random.sample(list(available_questions.values_list("id", flat=True)), n)

            with transaction.atomic():
                quiz = Quiz.objects.create(evaluation=evaluation, user=student, state="started")
                QuizResponse.objects.bulk_create(
                    [
                        QuizResponse(quiz=quiz, question_id=q_id, answer=None, score=None, done=None)
                        for q_id in selected_ids
                    ]
                )

        # Create or reuse launch for this quiz (idempotency)
        launch = (
            ExamLaunch.objects.filter(company_id=company.id, quiz_id=quiz.id, completed_at__isnull=True)
            .order_by("-created_at")
            .first()
        )
        if not launch:
            launch = ExamLaunch.objects.create(
                company_id=company.id,
                student_id=student.id,
                student_uuid=student_uuid,
                student_mobile=mobile,
                eurl=eurl,
                quiz_id=quiz.id,
                callback_url=callback_url,
            )
        else:
            launch.callback_url = callback_url
            launch.student_mobile = mobile
            launch.save(update_fields=["callback_url", "student_mobile"])

        # Call /api/quizzes/start/ endpoint internally
        quiz_id_from_start = quiz.id
        try:
            # Use APIClient to make internal API call
            api_client = APIClient()
            api_client.force_authenticate(user=student)
            
            # Make POST request to /api/quizzes/start/
            response = api_client.post(
                '/api/quizzes/start/',
                {'evaluation_id': eurl},
                format='json'
            )
            
            # Extract quiz_id from response if successful
            if response.status_code in [status.HTTP_200_OK, status.HTTP_201_CREATED]:
                response_data = response.data
                if 'quiz' in response_data and 'id' in response_data['quiz']:
                    quiz_id_from_start = response_data['quiz']['id']
        except Exception as e:
            # If internal call fails, use the existing quiz_id
            # Log the error but don't fail the launch
            pass

        base = getattr(settings, "EXAM_FRONT_BASE_URL", "") or ""
        exam_url = f"{base}?launch={launch.uuid}" if base else None
        
        return Response(
            {
                "launch_id": str(launch.uuid),
                "exam_url": exam_url,
                "quiz_id": quiz_id_from_start,
                "eurl": eurl,
                "student": {"uuid": student_uuid, "mobile": mobile},
                "is_existing_quiz": is_existing,
            },
            status=status.HTTP_201_CREATED,
        )


class LaunchDetailView(APIView):
    """
    Student-facing: fetch quiz questions by quiz_id.
    """

    authentication_classes = [ClientTokenAuthentication]
    permission_classes = [IsClientTokenAuthenticated]

    def get(self, request, quiz_id):
        try:
            quiz = Quiz.objects.select_related("evaluation", "user").prefetch_related("responses", "responses__question").get(id=quiz_id)
        except Quiz.DoesNotExist:
            return Response({"error": "Quiz یافت نشد"}, status=status.HTTP_404_NOT_FOUND)

        # Find active launch for this quiz
        launch = ExamLaunch.objects.filter(quiz_id=quiz_id, completed_at__isnull=True).order_by("-created_at").first()
        if not launch:
            return Response({"error": "Launch یافت نشد"}, status=status.HTTP_404_NOT_FOUND)
        
        # Ensure launch belongs to the same company as client token
        if launch.company_id != request.auth_company.id:
            return Response({"error": "دسترسی به این آزمون مجاز نیست"}, status=status.HTTP_403_FORBIDDEN)

        # Collect questions with current answers
        questions = Question.objects.filter(quiz_responses__quiz=quiz).distinct()
        questions_data = QuestionForQuizSerializer(questions, many=True).data

        responses_dict = {r.question_id: {"answer": r.answer, "done": r.done} for r in quiz.responses.all()}
        for q in questions_data:
            qid = q["id"]
            q["current_answer"] = responses_dict.get(qid, {}).get("answer")
            q["done"] = responses_dict.get(qid, {}).get("done")

        return Response(
            {
                "launch_id": str(launch.uuid),
                "quiz_id": quiz.id,
                "eurl": launch.eurl,
                "student": {"uuid": launch.student_uuid, "mobile": launch.student_mobile},
                "evaluation": {
                    "eurl": quiz.evaluation_id,
                    "title": quiz.evaluation.title,
                    "accept_score": quiz.evaluation.accept_score,
                    "duration": quiz.evaluation.duration,
                    "can_back": quiz.evaluation.can_back,
                    "number_of_question": quiz.evaluation.number_of_question,
                },
                "state": quiz.state,
                "start_at": quiz.start_at,
                "end_at": quiz.end_at,
                "questions": questions_data,
            },
            status=status.HTTP_200_OK,
        )


class LaunchAnswerView(APIView):
    """
    Student-facing: save one answer (optional convenience).
    """

    authentication_classes = [ClientTokenAuthentication]
    permission_classes = [IsClientTokenAuthenticated]

    def post(self, request, quiz_id):
        serializer = LaunchAnswerSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        try:
            quiz = Quiz.objects.get(id=quiz_id)
        except Quiz.DoesNotExist:
            return Response({"error": "Quiz یافت نشد"}, status=status.HTTP_404_NOT_FOUND)

        # Find active launch for this quiz
        launch = ExamLaunch.objects.filter(quiz_id=quiz_id, completed_at__isnull=True).order_by("-created_at").first()
        if not launch:
            return Response({"error": "Launch یافت نشد"}, status=status.HTTP_404_NOT_FOUND)
        
        # Ensure launch belongs to the same company as client token
        if launch.company_id != request.auth_company.id:
            return Response({"error": "دسترسی به این آزمون مجاز نیست"}, status=status.HTTP_403_FORBIDDEN)

        if quiz.end_at is not None:
            return Response({"error": "این آزمون قبلاً تمام شده است"}, status=status.HTTP_400_BAD_REQUEST)

        question_id = serializer.validated_data["question_id"]
        answer = serializer.validated_data.get("answer")
        done = serializer.validated_data.get("done")

        qr = QuizResponse.objects.filter(quiz_id=quiz.id, question_id=question_id).first()
        if not qr:
            return Response({"error": "این سوال متعلق به این آزمون نیست"}, status=status.HTTP_400_BAD_REQUEST)

        qr.answer = answer if answer != "" else None
        if done is not None:
            qr.done = done
        qr.save(update_fields=["answer", "done"])

        return Response({"message": "ذخیره شد"}, status=status.HTTP_200_OK)


class LaunchSubmitView(APIView):
    """
    Student-facing: submit all answers, finalize quiz, compute score, and return redirect_url for callback.
    """

    authentication_classes = [ClientTokenAuthentication]
    permission_classes = [IsClientTokenAuthenticated]

    def post(self, request, quiz_id):
        serializer = LaunchSubmitSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        try:
            quiz = Quiz.objects.select_related("evaluation", "user").get(id=quiz_id)
        except Quiz.DoesNotExist:
            return Response({"error": "Quiz یافت نشد"}, status=status.HTTP_404_NOT_FOUND)

        # Find active launch for this quiz
        launch = ExamLaunch.objects.filter(quiz_id=quiz_id, completed_at__isnull=True).order_by("-created_at").first()
        if not launch:
            return Response({"error": "Launch یافت نشد"}, status=status.HTTP_404_NOT_FOUND)
        
        # Ensure launch belongs to the same company as client token
        if launch.company_id != request.auth_company.id:
            return Response({"error": "دسترسی به این آزمون مجاز نیست"}, status=status.HTTP_403_FORBIDDEN)

        # Idempotent: if already finished, return cached result
        if quiz.end_at is not None and launch.completed_at is not None:
            redirect_url = _build_callback_url(
                launch.callback_url,
                {
                    "student_uuid": launch.student_uuid,
                    "mobile": launch.student_mobile,
                    "eurl": launch.eurl,
                    "quiz_id": launch.quiz_id,
                    "percentage": launch.percentage,
                    "total_score": launch.total_score,
                    "is_accept": launch.is_accept,
                    "state": launch.state,
                    "launch_id": str(launch.uuid),
                },
            )
            return Response(
                {
                    "message": "قبلاً ثبت شده است",
                    "result": {
                        "quiz_id": quiz.id,
                        "percentage": launch.percentage,
                        "total_score": launch.total_score,
                        "is_accept": launch.is_accept,
                        "state": launch.state,
                    },
                    "redirect_url": redirect_url,
                },
                status=status.HTTP_200_OK,
            )

        if quiz.end_at is not None:
            return Response({"error": "این آزمون قبلاً تمام شده است"}, status=status.HTTP_400_BAD_REQUEST)

        responses_data = serializer.validated_data["responses"]

        quiz_questions = Question.objects.filter(quiz_responses__quiz=quiz).distinct()
        if len(responses_data) != quiz_questions.count():
            return Response(
                {"error": "تعداد پاسخ‌های ارسالی با تعداد سوالات مطابقت ندارد"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            with transaction.atomic():
                total_score = 0.0
                correct_count = 0
                wrong_count = 0
                multiple_choice_count = 0

                for r in responses_data:
                    qid = r["question_id"]
                    student_answer = r.get("answer")
                    done = r.get("done", "completed")

                    question = Question.objects.filter(id=qid, evaluation=quiz.evaluation).first()
                    if not question:
                        continue

                    qr = QuizResponse.objects.filter(quiz=quiz, question=question).first()
                    if not qr:
                        qr = QuizResponse.objects.create(quiz=quiz, question=question, answer=None, score=None, done=None)

                    score = 0.0
                    if question.type:  # multiple choice
                        multiple_choice_count += 1
                        try:
                            ans_int = int(student_answer) if student_answer is not None and student_answer != "" else None
                        except (ValueError, TypeError):
                            ans_int = None

                        if ans_int is not None and question.correct is not None:
                            if ans_int == question.correct:
                                correct_count += 1
                                score = question.weight if question.weight else 1.0
                            else:
                                wrong_count += 1

                        qr.answer = str(ans_int) if ans_int is not None else None
                    else:
                        qr.answer = student_answer if student_answer else None
                        score = 0.0

                    qr.score = score
                    qr.done = done
                    qr.save()

                    total_score += score

                percentage = (correct_count / multiple_choice_count * 100) if multiple_choice_count > 0 else 0
                is_accept = percentage >= quiz.evaluation.accept_score if quiz.evaluation.accept_score else False

                quiz.end_at = timezone.now()
                quiz.score = total_score
                quiz.is_accept = is_accept
                if quiz.evaluation.type_id in (1, 3):
                    quiz.state = "completed"
                elif quiz.evaluation.type_id in (2, 4):
                    quiz.state = "pending"
                else:
                    quiz.state = quiz.state or "completed"
                quiz.save()

                QuizResponseEvaluation.objects.update_or_create(
                    user=quiz.user,
                    quiz=quiz,
                    defaults={"score": round(percentage, 2)},
                )

                if is_accept and quiz.evaluation.mission:
                    from roadmap_app.models import MissionResult

                    MissionResult.objects.update_or_create(
                        mission=quiz.evaluation.mission,
                        user=quiz.user,
                        quiz_id=quiz.id,
                        defaults={"state": "completed", "user_grant": None},
                    )

                # Cache on launch
                launch.completed_at = quiz.end_at
                launch.percentage = round(percentage, 2)
                launch.total_score = round(total_score, 2)
                launch.is_accept = bool(is_accept)
                launch.state = quiz.state
                launch.save(update_fields=["completed_at", "percentage", "total_score", "is_accept", "state"])

                final_responses = QuizResponse.objects.filter(quiz=quiz).select_related("question")

                result = {
                    "quiz_id": quiz.id,
                    "total_questions": quiz_questions.count(),
                    "correct_answers": correct_count,
                    "wrong_answers": wrong_count,
                    "percentage": round(percentage, 2),
                    "total_score": round(total_score, 2),
                    "is_accept": bool(is_accept),
                    "state": quiz.state,
                    "responses": QuizResponseSerializer(final_responses, many=True).data,
                }

        except Exception as e:
            return Response({"error": f"خطا در ثبت پاسخ‌ها: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        redirect_url = _build_callback_url(
            launch.callback_url,
            {
                "student_uuid": launch.student_uuid,
                "mobile": launch.student_mobile,
                "eurl": launch.eurl,
                "quiz_id": launch.quiz_id,
                "percentage": launch.percentage,
                "total_score": launch.total_score,
                "is_accept": launch.is_accept,
                "state": launch.state,
                "launch_id": str(launch.uuid),
            },
        )

        return Response(
            {"message": "پاسخ‌ها ثبت و آزمون پایان یافت", "result": result, "redirect_url": redirect_url},
            status=status.HTTP_200_OK,
        )


class LaunchRedirectView(APIView):
    """
    Browser redirect to customer's callback_url with result as query params.
    """

    authentication_classes = [ClientTokenAuthentication]
    permission_classes = [IsClientTokenAuthenticated]

    def get(self, request, quiz_id):
        try:
            quiz = Quiz.objects.get(id=quiz_id)
        except Quiz.DoesNotExist:
            return Response({"error": "Quiz یافت نشد"}, status=status.HTTP_404_NOT_FOUND)

        # Find completed launch for this quiz
        launch = ExamLaunch.objects.filter(quiz_id=quiz_id, completed_at__isnull=False).order_by("-created_at").first()
        if not launch:
            return Response({"error": "Launch یافت نشد"}, status=status.HTTP_404_NOT_FOUND)
        
        # Ensure launch belongs to the same company as client token
        if launch.company_id != request.auth_company.id:
            return Response({"error": "دسترسی به این آزمون مجاز نیست"}, status=status.HTTP_403_FORBIDDEN)

        if not launch.completed_at:
            return Response({"error": "آزمون هنوز تمام نشده است"}, status=status.HTTP_400_BAD_REQUEST)

        redirect_url = _build_callback_url(
            launch.callback_url,
            {
                "student_uuid": launch.student_uuid,
                "mobile": launch.student_mobile,
                "eurl": launch.eurl,
                "quiz_id": launch.quiz_id,
                "percentage": launch.percentage,
                "total_score": launch.total_score,
                "is_accept": launch.is_accept,
                "state": launch.state,
                "launch_id": str(launch.uuid),
            },
        )

        return HttpResponseRedirect(redirect_url)

