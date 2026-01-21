# Generated manually to fix token_blacklist foreign key constraint

from django.db import migrations


def fix_token_blacklist_foreign_key(apps, schema_editor):
    """Fix the foreign key constraint to point to our custom User model"""
    with schema_editor.connection.cursor() as cursor:
        # Drop the old foreign key constraint if it exists
        cursor.execute("""
            DO $$
            BEGIN
                IF EXISTS (
                    SELECT 1 FROM information_schema.table_constraints 
                    WHERE constraint_name = 'token_blacklist_outs_user_id_83bc629a_fk_auth_user'
                ) THEN
                    ALTER TABLE token_blacklist_outstandingtoken 
                    DROP CONSTRAINT token_blacklist_outs_user_id_83bc629a_fk_auth_user;
                END IF;
            END $$;
        """)
        
        # Check if the new constraint already exists, if not, create it
        cursor.execute("""
            DO $$
            BEGIN
                IF NOT EXISTS (
                    SELECT 1 FROM information_schema.table_constraints 
                    WHERE constraint_name = 'token_blacklist_outs_user_id_fk_users_app_user'
                ) THEN
                    ALTER TABLE token_blacklist_outstandingtoken 
                    ADD CONSTRAINT token_blacklist_outs_user_id_fk_users_app_user 
                    FOREIGN KEY (user_id) 
                    REFERENCES "user" (id) 
                    ON DELETE CASCADE;
                END IF;
            END $$;
        """)


def reverse_fix_token_blacklist_foreign_key(apps, schema_editor):
    """Reverse the migration"""
    with schema_editor.connection.cursor() as cursor:
        cursor.execute("""
            DO $$
            BEGIN
                IF EXISTS (
                    SELECT 1 FROM information_schema.table_constraints 
                    WHERE constraint_name = 'token_blacklist_outs_user_id_fk_users_app_user'
                ) THEN
                    ALTER TABLE token_blacklist_outstandingtoken 
                    DROP CONSTRAINT token_blacklist_outs_user_id_fk_users_app_user;
                END IF;
            END $$;
        """)


class Migration(migrations.Migration):

    dependencies = [
        ('kebrit_api', '0001_initial_django_schema'),
        ('token_blacklist', '0013_alter_blacklistedtoken_options_and_more'),
    ]

    operations = [
        migrations.RunPython(
            fix_token_blacklist_foreign_key,
            reverse_fix_token_blacklist_foreign_key
        ),
    ]

