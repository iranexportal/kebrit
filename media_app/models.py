import uuid
from django.db import models
from users_app.models import User, Company


class File(models.Model):
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='userId', related_name='files', null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, db_column='companyId', related_name='files', null=True, blank=True)
    product_id = models.IntegerField(db_column='productId', null=True, blank=True)
    file_name = models.CharField(db_column='fileName', max_length=255)
    file_type = models.CharField(db_column='fileType', max_length=50)
    file_size = models.BigIntegerField(db_column='fileSize', null=True, blank=True)
    path = models.TextField()
    bucket = models.CharField(max_length=255, null=True, blank=True)
    url = models.TextField(null=True, blank=True)
    is_public = models.BooleanField(db_column='isPublic', default=False)
    created_at = models.DateTimeField(db_column='createdAt', auto_now_add=True)

    class Meta:
        db_table = 'media.file'
        managed = True
        app_label = 'media_app'
        indexes = [
            models.Index(fields=['company'], name='idx_file_companyId'),
            models.Index(fields=['user'], name='idx_file_userId'),
        ]

    def __str__(self):
        return self.file_name


class Tag(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)

    class Meta:
        db_table = 'media.tag'
        managed = True
        app_label = 'media_app'

    def __str__(self):
        return self.title


class FileTag(models.Model):
    file = models.ForeignKey(File, on_delete=models.CASCADE, db_column='fileId', related_name='file_tags')
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, db_column='tagId', related_name='file_tags')

    class Meta:
        db_table = 'media.fileTag'
        managed = True
        app_label = 'media_app'
        unique_together = [['file', 'tag']]

    def __str__(self):
        return f"{self.file.file_name} - {self.tag.title}"
