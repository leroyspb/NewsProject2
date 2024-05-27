import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'news_project.settings')

app = Celery('news_project')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'print_every_5_seconds': {
        'task': 'tasks.digit',
        'schedule': 5,
        'args': (5, 2)
    }
}

