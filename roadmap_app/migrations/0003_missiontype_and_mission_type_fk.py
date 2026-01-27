from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('roadmap_app', '0002_alter_ability_table_alter_mission_table_and_more'),
    ]

    # این مایگریشن عمداً خالی شده است تا تغییری روی دیتابیس اعمال نکند.
    # جدول missiontype و تغییرات وابسته، مستقیماً در schema‌ی پایگاه‌داده (مثلاً roadmap) مدیریت می‌شوند.
    operations = []

