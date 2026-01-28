from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from users_app.models import Company, User
from roadmap_app.models import Mission
from exam_app.models import EvaluationType, Evaluation, Quiz, QuizResponseEvaluation
from kebrit_api.models import ClientApiToken


class MissionStudentReportAPITests(APITestCase):
    """
    تست‌های endpoint:
    POST /api/mission-student-report/
    """

    def setUp(self):
        self.client = APIClient()

        # ساخت داده‌های پایه: شرکت، توکن مشتری، کاربر (دانشجو)، ماموریت و آزمون
        self.company = Company.objects.create(name="Test Company")
        self.client_token = ClientApiToken.objects.create(company=self.company, name="Test Token")

        self.student_mobile = "09123456789"
        self.student = User.objects.create(
            uuid="test-uuid",
            username="student1",
            company=self.company,
            mobile=self.student_mobile,
            name="Test Student",
        )

        self.mission = Mission.objects.create(
            company=self.company,
            user=self.student,
            type="A",
            title="Test Mission",
            content="Test content",
            mo=True,
            point=100,
        )

        self.eval_type = EvaluationType.objects.create(title="Quiz")
        self.evaluation = Evaluation.objects.create(
            title="Test Evaluation",
            type=self.eval_type,
            accept_score=60,
            number_of_question=10,
            mission=self.mission,
            user=self.student,
        )

        # یک کوئیز تمام‌شده برای این دانشجو و این ماموریت
        self.quiz = Quiz.objects.create(
            evaluation=self.evaluation,
            user=self.student,
            score=17.0,
            is_accept=True,
            state="completed",
        )
        self.qre = QuizResponseEvaluation.objects.create(
            user=self.student,
            quiz=self.quiz,
            score=85.0,
        )

        self.url = "/api/mission-student-report/"
        self.auth_headers = {
            "HTTP_X_CLIENT_TOKEN": str(self.client_token.uuid)
        }

    def test_mission_student_report_success_with_erul(self):
        """
        درخواست موفق با بدنه:
        {
          "mobile": "...",
          "erul": <evaluation.id>
        }
        """
        payload = {
            "mobile": self.student_mobile,
            "erul": self.evaluation.id,
        }

        response = self.client.post(self.url, data=payload, format="json", **self.auth_headers)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()

        self.assertEqual(data["mission_id"], self.mission.id)
        self.assertEqual(data["mobile"], self.student_mobile)
        self.assertEqual(data["user_id"], self.student.id)
        self.assertIsInstance(data.get("attempts"), list)
        self.assertGreaterEqual(len(data["attempts"]), 1)

        first_attempt = data["attempts"][0]
        self.assertEqual(first_attempt["evaluation_id"], self.evaluation.id)
        self.assertEqual(first_attempt["quiz_id"], self.quiz.id)

    def test_mission_student_report_missing_erul_returns_400(self):
        """
        اگر فیلد erul ارسال نشود باید 400 برگردد.
        """
        payload = {
            "mobile": self.student_mobile,
            # "erul" عمداً ارسال نمی‌شود
        }

        response = self.client.post(self.url, data=payload, format="json", **self.auth_headers)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        data = response.json()
        self.assertIn("erul", data.get("error", {}))

    def test_mission_student_report_invalid_erul_returns_404(self):
        """
        اگر erul به evaluation معتبر (در همان شرکت) اشاره نکند باید 404 برگردد.
        """
        payload = {
            "mobile": self.student_mobile,
            "erul": 999999,  # شناسه‌ای که وجود ندارد
        }

        response = self.client.post(self.url, data=payload, format="json", **self.auth_headers)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class UserMissionsAPITests(APITestCase):
    """
    تست ساده برای endpoint:
    POST /api/user-missions/
    برای اطمینان از اینکه روی لوکال قابل فراخوانی است.
    """

    def setUp(self):
        self.client = APIClient()

        self.company = Company.objects.create(name="Test Company")
        self.client_token = ClientApiToken.objects.create(company=self.company, name="Test Token")

        self.student_mobile = "09120000000"
        self.student = User.objects.create(
            uuid="user-missions-uuid",
            username="student2",
            company=self.company,
            mobile=self.student_mobile,
            name="User Missions Student",
        )

        self.url = "/api/user-missions/"
        self.auth_headers = {
            "HTTP_X_CLIENT_TOKEN": str(self.client_token.uuid)
        }

    def test_user_missions_basic_structure(self):
        """
        فقط ساختار کلی پاسخ را چک می‌کند (بدون الزام به وجود ماموریت).
        """
        payload = {
            "mobile": self.student_mobile,
        }

        response = self.client.post(self.url, data=payload, format="json", **self.auth_headers)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()

        self.assertIn("user", data)
        self.assertIn("completed_missions", data)
        self.assertIn("available_missions", data)
        self.assertIn("stats", data)
