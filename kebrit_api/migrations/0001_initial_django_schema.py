"""
Migration to create django schema and move Django tables to it
Run this migration after creating the schema in PostgreSQL
"""
from django.db import migrations


def create_django_schema(apps, schema_editor):
    """Create django schema if it doesn't exist"""
    with schema_editor.connection.cursor() as cursor:
        cursor.execute("CREATE SCHEMA IF NOT EXISTS django;")
        cursor.execute("GRANT ALL PRIVILEGES ON SCHEMA django TO CURRENT_USER;")


def reverse_create_django_schema(apps, schema_editor):
    """Drop django schema (be careful!)"""
    with schema_editor.connection.cursor() as cursor:
        cursor.execute("DROP SCHEMA IF EXISTS django CASCADE;")


class Migration(migrations.Migration):

    dependencies = []

    operations = [
        migrations.RunPython(create_django_schema, reverse_create_django_schema),
    ]

