# Generated migration for adding title field to Evaluation

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exam_app', '0003_alter_quizresponseevaluation_quiz'),
    ]

    operations = [
        # Note: Since models are unmanaged (managed=False), 
        # the actual database schema changes need to be done manually via SQL:
        # 
        # ALTER TABLE exam.evaluation 
        # ADD COLUMN IF NOT EXISTS title VARCHAR(255);
        
        migrations.RunSQL(
            sql="""
                -- Add title column to evaluation table
                ALTER TABLE exam.evaluation 
                ADD COLUMN IF NOT EXISTS title VARCHAR(255);
            """,
            reverse_sql="""
                -- Reverse migration: remove title column
                ALTER TABLE exam.evaluation 
                DROP COLUMN IF EXISTS title;
            """
        ),
    ]

