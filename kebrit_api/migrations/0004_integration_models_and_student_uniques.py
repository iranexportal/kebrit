import uuid

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('kebrit_api', '0003_drop_user_password'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClientApiToken',
            fields=[
                ('uuid', models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, serialize=False)),
                ('name', models.CharField(max_length=100, null=True, blank=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('allowed_callback_hosts', models.TextField(null=True, blank=True)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users_app.company', related_name='api_tokens', db_constraint=False)),
            ],
            options={
                'db_table': 'client_api_token',
            },
        ),
        migrations.CreateModel(
            name='ExamLaunch',
            fields=[
                ('uuid', models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, serialize=False)),
                ('company_id', models.IntegerField()),
                ('student_id', models.IntegerField()),
                ('student_uuid', models.CharField(max_length=255)),
                ('student_mobile', models.CharField(max_length=20)),
                ('eurl', models.IntegerField()),
                ('quiz_id', models.IntegerField()),
                ('callback_url', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('completed_at', models.DateTimeField(null=True, blank=True)),
                ('percentage', models.FloatField(null=True, blank=True)),
                ('total_score', models.FloatField(null=True, blank=True)),
                ('is_accept', models.BooleanField(null=True, blank=True)),
                ('state', models.CharField(max_length=50, null=True, blank=True)),
            ],
            options={
                'db_table': 'exam_launch',
            },
        ),
        migrations.AddIndex(
            model_name='clientapitoken',
            index=models.Index(fields=['company'], name='idx_clientToken_companyId'),
        ),
        migrations.AddIndex(
            model_name='clientapitoken',
            index=models.Index(fields=['is_active'], name='idx_clientToken_isActive'),
        ),
        migrations.AddIndex(
            model_name='examlaunch',
            index=models.Index(fields=['company_id'], name='idx_examLaunch_companyId'),
        ),
        migrations.AddIndex(
            model_name='examlaunch',
            index=models.Index(fields=['quiz_id'], name='idx_examLaunch_quizId'),
        ),
        migrations.AddIndex(
            model_name='examlaunch',
            index=models.Index(fields=['eurl'], name='idx_examLaunch_eurl'),
        ),
        migrations.RunSQL(
            sql=r"""
DO $$
DECLARE r record;
BEGIN
  -- Drop UNIQUE constraints on users."user"(mobile) if any (students can exist across multiple companies)
  FOR r IN
    SELECT c.conname
    FROM pg_constraint c
    JOIN pg_class t ON c.conrelid = t.oid
    JOIN pg_namespace n ON t.relnamespace = n.oid
    WHERE n.nspname = 'users'
      AND t.relname = 'user'
      AND c.contype = 'u'
      AND pg_get_constraintdef(c.oid) ILIKE '%(mobile)%'
  LOOP
    EXECUTE format('ALTER TABLE users."user" DROP CONSTRAINT IF EXISTS %I;', r.conname);
  END LOOP;

  -- Drop UNIQUE indexes on mobile (if any) that are not constraints
  FOR r IN
    SELECT indexname
    FROM pg_indexes
    WHERE schemaname = 'users'
      AND tablename = 'user'
      AND indexdef ILIKE '%unique%'
      AND indexdef ILIKE '%(mobile)%'
  LOOP
    EXECUTE format('DROP INDEX IF EXISTS users.%I;', r.indexname);
  END LOOP;
END $$;

-- Ensure student uniqueness per company (uuid is provided by customer's system)
CREATE UNIQUE INDEX IF NOT EXISTS idx_user_company_uuid_unique ON users."user"(companyid, uuid);

-- Helpful lookup indexes
CREATE INDEX IF NOT EXISTS idx_user_company_mobile ON users."user"(companyid, mobile);
CREATE INDEX IF NOT EXISTS idx_user_mobile ON users."user"(mobile);
""",
            reverse_sql=migrations.RunSQL.noop,
        ),
    ]

