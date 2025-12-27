from django.db import models
from users_app.models import User
from roadmap_app.models import Mission


class Evaluation(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.BooleanField()
    accept_score = models.IntegerField(db_column='acceptscore')
    number_of_question = models.IntegerField(db_column='numberofquestion')
    mission = models.ForeignKey(Mission, on_delete=models.CASCADE, db_column='missionid', related_name='evaluations', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='userid', related_name='evaluations', null=True, blank=True)
    create_at = models.DateTimeField(db_column='createat', auto_now_add=True)
    is_active = models.BooleanField(db_column='isactive', default=True)
    can_back = models.BooleanField(db_column='canback', default=True)
    duration = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'evaluation'
        managed = False
        app_label = 'exam_app'
        indexes = [
            models.Index(fields=['mission'], name='idx_evaluation_missionId'),
            models.Index(fields=['user'], name='idx_evaluation_userId'),
        ]

    def __str__(self):
        return f"Evaluation {self.id}"


class Question(models.Model):
    id = models.AutoField(primary_key=True)
    evaluation = models.ForeignKey(Evaluation, on_delete=models.CASCADE, db_column='evaluationid', related_name='questions')
    description = models.TextField()
    img = models.CharField(max_length=255, null=True, blank=True)
    type = models.BooleanField()
    c1 = models.TextField(null=True, blank=True)
    c2 = models.TextField(null=True, blank=True)
    c3 = models.TextField(null=True, blank=True)
    c4 = models.TextField(null=True, blank=True)
    correct = models.IntegerField(null=True, blank=True)
    answer = models.TextField(null=True, blank=True)
    weight = models.FloatField(null=True, blank=True)
    can_shuffle = models.BooleanField(db_column='canshuffle', default=False)

    class Meta:
        db_table = 'question'
        managed = False
        app_label = 'exam_app'
        indexes = [
            models.Index(fields=['evaluation'], name='idx_question_evaluationId'),
        ]

    def __str__(self):
        return f"Question {self.id} for Evaluation {self.evaluation_id}"


class Quiz(models.Model):
    id = models.AutoField(primary_key=True)
    evaluation = models.ForeignKey(Evaluation, on_delete=models.CASCADE, db_column='evaluationid', related_name='quizzes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='userid', related_name='quizzes')
    start_at = models.DateTimeField(db_column='startat', auto_now_add=True)
    end_at = models.DateTimeField(db_column='endat', null=True, blank=True)
    score = models.FloatField(null=True, blank=True)
    is_accept = models.BooleanField(db_column='isaccept', null=True, blank=True)
    state = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        db_table = 'quiz'
        managed = False
        app_label = 'exam_app'
        indexes = [
            models.Index(fields=['evaluation'], name='idx_quiz_evaluationId'),
            models.Index(fields=['user'], name='idx_quiz_userId'),
        ]

    def __str__(self):
        return f"Quiz {self.id} for User {self.user_id}"


class QuizResponse(models.Model):
    id = models.AutoField(primary_key=True)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, db_column='quizid', related_name='responses')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, db_column='questionid', related_name='quiz_responses')
    answer = models.IntegerField(null=True, blank=True)
    score = models.FloatField(null=True, blank=True)
    done = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'quizresponse'
        managed = False
        app_label = 'exam_app'
        indexes = [
            models.Index(fields=['quiz'], name='idx_quizResponse_quizId'),
            models.Index(fields=['question'], name='idx_quizResponse_questionId'),
        ]

    def __str__(self):
        return f"QuizResponse {self.id} for Quiz {self.quiz_id}"


class QuizResponseEvaluation(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='userid', related_name='quiz_response_evaluations')
    quiz_response = models.ForeignKey(QuizResponse, on_delete=models.CASCADE, db_column='quizresponseid', related_name='evaluations')
    score = models.FloatField(null=True, blank=True)

    class Meta:
        db_table = 'quizresponseevaluation'
        managed = False
        app_label = 'exam_app'
        indexes = [
            models.Index(fields=['user'], name='idx_qre_userId'),
            models.Index(fields=['quiz_response'], name='idx_qre_quizRespId'),
        ]

    def __str__(self):
        return f"QuizResponseEvaluation {self.id}"
