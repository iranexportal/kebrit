from django.contrib import admin
from .models import File, Tag, FileTag


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ['id', 'uuid', 'file_name', 'file_type', 'file_size', 'company', 'user', 'is_public', 'created_at']
    list_filter = ['file_type', 'is_public', 'company', 'created_at']
    search_fields = ['file_name', 'uuid', 'path']
    raw_id_fields = ['company', 'user']
    date_hierarchy = 'created_at'
    readonly_fields = ['uuid', 'created_at']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']
    search_fields = ['title']


@admin.register(FileTag)
class FileTagAdmin(admin.ModelAdmin):
    list_display = ['id', 'file', 'tag']
    list_filter = ['tag']
    search_fields = ['file__file_name', 'tag__title']
    raw_id_fields = ['file', 'tag']
