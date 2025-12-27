from django.db import models
from users_app.models import User, Company


class Mission(models.Model):
    id = models.AutoField(primary_key=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, db_column='companyid', related_name='missions', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='userid', related_name='missions', null=True, blank=True)
    type = models.CharField(max_length=1)
    title = models.CharField(max_length=255)
    content = models.TextField()
    mo = models.BooleanField()
    point = models.IntegerField()
    create_at = models.DateTimeField(db_column='createat', auto_now_add=True)
    modified_at = models.DateTimeField(db_column='modifiedat', null=True, blank=True)
    expier_at = models.DateTimeField(db_column='expierat', null=True, blank=True)
    is_active = models.BooleanField(db_column='isactive', default=True)
    at_least_point = models.IntegerField(db_column='atleastpoint', null=True, blank=True)

    class Meta:
        db_table = 'mission'
        managed = False
        app_label = 'roadmap_app'
        indexes = [
            models.Index(fields=['company'], name='idx_mission_companyId'),
            models.Index(fields=['user'], name='idx_mission_userId'),
        ]

    def __str__(self):
        return self.title


class MissionRelation(models.Model):
    id = models.AutoField(primary_key=True)
    mission = models.ForeignKey(Mission, on_delete=models.CASCADE, db_column='missionid', related_name='relations')
    parent = models.ForeignKey(Mission, on_delete=models.CASCADE, db_column='parentid', related_name='child_relations', null=True, blank=True)
    child = models.ForeignKey(Mission, on_delete=models.CASCADE, db_column='childid', related_name='parent_relations', null=True, blank=True)

    class Meta:
        db_table = 'missionrelation'
        managed = False
        app_label = 'roadmap_app'
        indexes = [
            models.Index(fields=['mission'], name='idx_missionRelation_missionId'),
        ]

    def __str__(self):
        return f"Mission {self.mission_id} Relation"


class Ability(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, db_column='companyid', related_name='abilities')

    class Meta:
        db_table = 'ability'
        managed = False
        app_label = 'roadmap_app'
        indexes = [
            models.Index(fields=['company'], name='idx_ability_companyId'),
        ]

    def __str__(self):
        return self.title


class MissionResult(models.Model):
    id = models.AutoField(primary_key=True)
    mission = models.ForeignKey(Mission, on_delete=models.CASCADE, db_column='missionid', related_name='results')
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='userid', related_name='mission_results')
    state = models.CharField(max_length=50)
    user_grant = models.IntegerField(db_column='usergrant', null=True, blank=True)
    quiz_id = models.IntegerField(db_column='quizid', null=True, blank=True)
    ability = models.ForeignKey(Ability, on_delete=models.CASCADE, db_column='abilityid', related_name='mission_results', null=True, blank=True)

    class Meta:
        db_table = 'missionresult'
        managed = False
        app_label = 'roadmap_app'
        indexes = [
            models.Index(fields=['mission'], name='idx_missionResult_missionId'),
            models.Index(fields=['user'], name='idx_missionResult_userId'),
        ]

    def __str__(self):
        return f"Mission {self.mission_id} Result for User {self.user_id}"
