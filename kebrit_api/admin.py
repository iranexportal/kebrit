from django.contrib import admin

from .models import ClientApiToken, ExamLaunch


@admin.register(ClientApiToken)
class ClientApiTokenAdmin(admin.ModelAdmin):
    list_display = ("uuid", "company", "name", "is_active", "created_at")
    list_filter = ("is_active", "company")
    search_fields = ("uuid", "name", "company__name")
    raw_id_fields = ("company",)


@admin.register(ExamLaunch)
class ExamLaunchAdmin(admin.ModelAdmin):
    list_display = ("uuid", "company_id", "eurl", "quiz_id", "student_uuid", "student_mobile", "created_at", "completed_at", "state")
    list_filter = ("state", "company_id")
    search_fields = ("uuid", "student_uuid", "student_mobile")

