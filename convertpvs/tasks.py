from celery import shared_task
from .schedular import scheduled



@shared_task
def schedule():
    result = scheduled()
    if result == 'success':
        return True
    else:
        return False