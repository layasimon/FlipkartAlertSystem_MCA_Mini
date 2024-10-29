# myproject/celery.py

from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

app = Celery('myproject')

# Configure Celery using Django's settings with a 'CELERY' namespace.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks from installed apps.
app.autodiscover_tasks()

# Add periodic task to Celery Beat
app.conf.beat_schedule = {
    'check-price-every-5-seconds': {
        'task': 'myapp.tasks.compare_price_and_notify',
        'schedule': 5.0,
    },
}
