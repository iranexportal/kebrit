from django.db import migrations


def fix_admin_log_user_foreign_key(apps, schema_editor):
    """
    Fix django_admin_log.user_id FK to reference our custom user table users."user"(id)
    instead of auth_user.
    """
    with schema_editor.connection.cursor() as cursor:
        cursor.execute(
            """
DO $$
BEGIN
  -- Drop old FK to auth_user if present
  IF EXISTS (
    SELECT 1 FROM information_schema.table_constraints
    WHERE constraint_name = 'django_admin_log_user_id_c564eba6_fk_auth_user_id'
  ) THEN
    ALTER TABLE django_admin_log
      DROP CONSTRAINT django_admin_log_user_id_c564eba6_fk_auth_user_id;
  END IF;

  -- Add FK to users."user" if missing
  IF NOT EXISTS (
    SELECT 1 FROM information_schema.table_constraints
    WHERE constraint_name = 'django_admin_log_user_id_fk_users_user'
  ) THEN
    ALTER TABLE django_admin_log
      ADD CONSTRAINT django_admin_log_user_id_fk_users_user
      FOREIGN KEY (user_id)
      REFERENCES users."user"(id)
      ON DELETE SET NULL;
  END IF;
END $$;
"""
        )


def reverse_fix_admin_log_user_foreign_key(apps, schema_editor):
    with schema_editor.connection.cursor() as cursor:
        cursor.execute(
            """
DO $$
BEGIN
  IF EXISTS (
    SELECT 1 FROM information_schema.table_constraints
    WHERE constraint_name = 'django_admin_log_user_id_fk_users_user'
  ) THEN
    ALTER TABLE django_admin_log
      DROP CONSTRAINT django_admin_log_user_id_fk_users_user;
  END IF;
END $$;
"""
        )


class Migration(migrations.Migration):

    dependencies = [
        ('kebrit_api', '0005_add_user_username_for_admin'),
    ]

    operations = [
        migrations.RunPython(fix_admin_log_user_foreign_key, reverse_fix_admin_log_user_foreign_key),
    ]

