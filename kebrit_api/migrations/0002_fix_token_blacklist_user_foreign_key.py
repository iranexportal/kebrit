# Generated manually to fix token_blacklist foreign key constraint
# NOTE: This migration is now a no-op since token_blacklist is no longer used

from django.db import migrations


def fix_token_blacklist_foreign_key(apps, schema_editor):
    """No-op: token_blacklist is no longer used"""
    pass


def reverse_fix_token_blacklist_foreign_key(apps, schema_editor):
    """No-op: token_blacklist is no longer used"""
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('kebrit_api', '0001_initial_django_schema'),
        # Removed dependency on token_blacklist since it's no longer used
    ]

    operations = [
        migrations.RunPython(
            fix_token_blacklist_foreign_key,
            reverse_fix_token_blacklist_foreign_key
        ),
    ]

