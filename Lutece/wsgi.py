"""
WSGI config for Lutece project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/
"""

import os
from threading import Thread
from django.core.wsgi import get_wsgi_application
from submission.tasks import init_push_waiting_submission, read_modify_status
from data_server.listen import run_data_server

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Lutece.settings")

application = get_wsgi_application()
init_push_waiting_submission()
Thread( target = run_data_server ).start()
Thread( target = read_modify_status ).start()