from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from Lutece.settings import rabbitmq_ip, rabbitmq_port, rabbitmq_user, rabbitmq_pwd, rabbitmq_vhost

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Lutece.settings')


BROKER_URL = 'pyamqp://{user}:{pwd}@{ip}:{port}/{vhost}'.format(
    user = rabbitmq_user,
    pwd = rabbitmq_pwd,
    ip = rabbitmq_ip,
    port = rabbitmq_port,
    vhost = rabbitmq_vhost)

app = Celery(
    name = 'Lutece',
    broker = BROKER_URL
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