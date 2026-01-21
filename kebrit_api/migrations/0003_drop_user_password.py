from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kebrit_api', '0002_fix_token_blacklist_user_foreign_key'),
    ]

    operations = [
        migrations.RunSQL(
            sql='ALTER TABLE IF EXISTS users."user" DROP COLUMN IF EXISTS password;',
            reverse_sql='ALTER TABLE IF EXISTS users."user" ADD COLUMN IF NOT EXISTS password varchar(255);',
        ),
    ]

