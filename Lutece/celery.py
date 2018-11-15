from __future__ import absolute_import, unicode_literals

import os
from celery import Celery

from judge.configure import RABBITMQ_IP, RABBITMQ_PORT, RABBITMQ_USER, RABBITMQ_PWD, RABBITMQ_VHOST

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Lutece.settings')

BROKER_URL = 'pyamqp://{user}:{pwd}@{ip}:{port}/{vhost}'.format(
    user=RABBITMQ_USER,
    pwd=RABBITMQ_PWD,
    ip=RABBITMQ_IP,
    port=RABBITMQ_PORT,
    vhost=RABBITMQ_VHOST)

app = Celery(
    name='Lutece',
    broker=BROKER_URL
)

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
