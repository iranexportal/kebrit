from django.db import models
from users_app.models import User, Company
from roadmap_app.models import Mission


class Level(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=100)
    order = models.IntegerField(unique=True)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    requiredpoints = models.IntegerField()
    icon = models.CharField(max_length=255, null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, db_column='companyid', related_name='levels', null=True, blank=True)
    isactive = models.BooleanField(db_column='isactive', default=True)

    class Meta:
        db_table = 'level'
        managed = False
        app_label = 'gaming_app'
        indexes = [
            models.Index(fields=['company'], name='idx_level_companyId'),
            models.Index(fields=['code'], name='idx_level_code'),
        ]

    def __str__(self):
        return f"{self.title} (Level {self.order})"


class UserLevel(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='userid', related_name='user_levels')
    level = models.ForeignKey(Level, on_delete=models.CASCADE, db_column='levelid', related_name='user_levels')
    currentpoints = models.IntegerField(db_column='currentpoints', default=0)
    reachedat = models.DateTimeField(db_column='reachedat')

    class Meta:
        db_table = 'userlevel'
        managed = False
        app_label = 'gaming_app'
        unique_together = [['user', 'level']]
        indexes = [
            models.Index(fields=['user'], name='idx_userLevel_userId'),
            models.Index(fields=['level'], name='idx_userLevel_levelId'),
        ]

    def __str__(self):
        return f"{self.user.name} - {self.level.title}"


class Badge(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=100)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    icon = models.CharField(max_length=255, null=True, blank=True)
    mission = models.ForeignKey(Mission, on_delete=models.SET_NULL, db_column='missionid', related_name='badges', null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, db_column='companyid', related_name='badges', null=True, blank=True)
    isactive = models.BooleanField(db_column='isactive', default=True)

    class Meta:
        db_table = 'badge'
        managed = False
        app_label = 'gaming_app'
        indexes = [
            models.Index(fields=['company'], name='idx_badge_companyId'),
            models.Index(fields=['mission'], name='idx_badge_missionId'),
            models.Index(fields=['code'], name='idx_badge_code'),
        ]

    def __str__(self):
        return self.title


class UserBadge(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='userid', related_name='user_badges')
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE, db_column='badgeid', related_name='user_badges')
    earnedat = models.DateTimeField(db_column='earnedat')

    class Meta:
        db_table = 'userbadge'
        managed = False
        app_label = 'gaming_app'
        unique_together = [['user', 'badge']]
        indexes = [
            models.Index(fields=['user'], name='idx_userBadge_userId'),
            models.Index(fields=['badge'], name='idx_userBadge_badgeId'),
        ]

    def __str__(self):
        return f"{self.user.name} - {self.badge.title}"


class UserPoint(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, db_column='userid', related_name='user_point')
    totalpoints = models.IntegerField(db_column='totalpoints', default=0)
    lastupdated = models.DateTimeField(db_column='lastupdated', null=True, blank=True)

    class Meta:
        db_table = 'userpoint'
        managed = False
        app_label = 'gaming_app'
        indexes = [
            models.Index(fields=['user'], name='idx_userPoint_userId'),
        ]

    def __str__(self):
        return f"{self.user.name} - {self.totalpoints} points"


class UserAction(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='userid', related_name='user_actions')
    actiontype = models.CharField(db_column='actiontype', max_length=100)
    pointsearned = models.IntegerField(db_column='pointsearned', default=0)
    description = models.TextField(null=True, blank=True)
    createdat = models.DateTimeField(db_column='createdat', auto_now_add=True)

    class Meta:
        db_table = 'useraction'
        managed = False
        app_label = 'gaming_app'
        indexes = [
            models.Index(fields=['user'], name='idx_userAction_userId'),
            models.Index(fields=['actiontype'], name='idx_userAction_actionType'),
            models.Index(fields=['createdat'], name='idx_userAction_createdAt'),
        ]

    def __str__(self):
        return f"{self.user.name} - {self.actiontype} ({self.pointsearned} points)"
