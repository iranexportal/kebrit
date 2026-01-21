import uuid

from django.db import models

from users_app.models import Company


class ClientApiToken(models.Model):
    """
    API token per customer (Company).
    Customers use this token in request headers to authenticate API calls.
    """

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='api_tokens', db_constraint=False)
    name = models.CharField(max_length=100, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # Optional allowlist for callback URLs (comma-separated hostnames)
    allowed_callback_hosts = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'client_api_token'
        app_label = 'kebrit_api'
        indexes = [
            models.Index(fields=['company'], name='idx_clientToken_companyId'),
            models.Index(fields=['is_active'], name='idx_clientToken_isActive'),
        ]

    def __str__(self):
        return f"{self.company_id}:{self.uuid}"


class ExamLaunch(models.Model):
    """
    One launch/session created by customer for a student to take an exam.
    The launch UUID is safe to be used in browser URLs.
    """

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # We store raw ids to avoid cross-schema FK complexities
    company_id = models.IntegerField()
    student_id = models.IntegerField()
    student_uuid = models.CharField(max_length=255)
    student_mobile = models.CharField(max_length=20)

    eurl = models.IntegerField()  # evaluation id (numeric)
    quiz_id = models.IntegerField()

    callback_url = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    # Cache final result for idempotent callbacks
    percentage = models.FloatField(null=True, blank=True)
    total_score = models.FloatField(null=True, blank=True)
    is_accept = models.BooleanField(null=True, blank=True)
    state = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        db_table = 'exam_launch'
        app_label = 'kebrit_api'
        indexes = [
            models.Index(fields=['company_id'], name='idx_examLaunch_companyId'),
            models.Index(fields=['quiz_id'], name='idx_examLaunch_quizId'),
            models.Index(fields=['eurl'], name='idx_examLaunch_eurl'),
        ]

    def __str__(self):
        return f"Launch {self.uuid} (quiz={self.quiz_id})"

