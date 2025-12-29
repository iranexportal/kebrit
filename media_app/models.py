import uuid
from django.db import models
from users_app.models import User, Company


class File(models.Model):
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='userid', related_name='files', null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, db_column='companyid', related_name='files', null=True, blank=True)
    product_id = models.IntegerField(db_column='productid', null=True, blank=True)
    file_name = models.CharField(db_column='filename', max_length=255)
    file_type = models.CharField(db_column='filetype', max_length=50)
    file_size = models.BigIntegerField(db_column='filesize', null=True, blank=True)
    path = models.TextField()
    bucket = models.CharField(max_length=255, null=True, blank=True)
    url = models.TextField(null=True, blank=True)
    is_public = models.BooleanField(db_column='ispublic', default=False)
    created_at = models.DateTimeField(db_column='createdat', auto_now_add=True)

    class Meta:
        db_table = 'file'
        managed = False
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
        db_table = 'tag'
        managed = False
        app_label = 'media_app'

    def __str__(self):
        return self.title


class FileTag(models.Model):
    # Note: This table uses composite primary key (fileid, tagid) in the database
    # Django requires an id field, but since managed=False, it won't be used in DB queries
    id = models.BigAutoField(primary_key=True)  # Django requirement for models without explicit primary key
    file = models.ForeignKey(File, on_delete=models.CASCADE, db_column='fileid', related_name='file_tags')
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, db_column='tagid', related_name='file_tags')

    class Meta:
        db_table = 'filetag'
        managed = False
        app_label = 'media_app'
        unique_together = [['file', 'tag']]

    def __str__(self):
        return f"{self.file.file_name} - {self.tag.title}"
