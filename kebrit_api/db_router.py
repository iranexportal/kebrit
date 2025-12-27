"""
Database router to place Django default tables in 'django' schema
"""
from django.conf import settings


class DjangoSchemaRouter:
    """
    Router to place Django default tables in 'django' schema
    """
    
    # Apps that should use django schema
    django_apps = {
        'admin',
        'auth',
        'contenttypes',
        'sessions',
        'messages',
        'staticfiles',
    }
    
    def db_for_read(self, model, **hints):
        """Suggest which database should be used for read operations."""
        if model._meta.app_label in self.django_apps:
            return 'default'
        return None
    
    def db_for_write(self, model, **hints):
        """Suggest which database should be used for write operations."""
        if model._meta.app_label in self.django_apps:
            return 'default'
        return None
    
    def allow_relation(self, obj1, obj2, **hints):
        """Allow relations if both models are in the same app."""
        return None
    
    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """Ensure Django default apps migrate to default database with django schema."""
        if app_label in self.django_apps:
            return db == 'default'
        return None

