from __future__ import absolute_import, unicode_literals
# from django_celery_beat.models import PeriodicTask, PeriodicTasks
import os
from celery import Celery
from celery.schedules import crontab
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ConvertPV.settings')

app = Celery('ConvertPV')
# app.conf.enable_utc = False

app.conf.update(timezone='Asia/Kolkata')

app.config_from_object(settings, namespace='CELERY')

# Celery Beat Settings
app.conf.beat_schedule = {
        'conversion': {
            'task': 'convertpvs.tasks.schedule',
            'schedule': crontab(hour='14', minute='*/1'),
        }
}

app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')