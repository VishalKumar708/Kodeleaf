from django.apps import AppConfig


class ConvertpvsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'convertpvs'
    verbose_name = 'ConvertPV'


class CeleryBeatConfig(AppConfig):
    name = 'django_celery_results'
    verbose_name = 'Django Celery results'
