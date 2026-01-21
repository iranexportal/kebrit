from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kebrit_api', '0004_integration_models_and_student_uniques'),
    ]

    operations = [
        migrations.RunSQL(
            sql=r"""
ALTER TABLE IF EXISTS users."user"
  ADD COLUMN IF NOT EXISTS username varchar(150);

-- Unique username for admin/internal users (students can leave it NULL)
CREATE UNIQUE INDEX IF NOT EXISTS idx_user_username_unique
  ON users."user"(username)
  WHERE username IS NOT NULL;

CREATE INDEX IF NOT EXISTS idx_user_username
  ON users."user"(username);
""",
            reverse_sql=r"""
DROP INDEX IF EXISTS users.idx_user_username;
DROP INDEX IF EXISTS users.idx_user_username_unique;
-- We keep the column by default to avoid destructive rollback.
""",
        ),
    ]

