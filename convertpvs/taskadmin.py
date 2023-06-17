# admin.py
from django.contrib import admin
from django_celery_beat.models import PeriodicTask



admin.site.register(PeriodicTask)