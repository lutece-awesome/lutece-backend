from __future__ import absolute_import, unicode_literals
from celery import shared_task
from time import sleep


@shared_task
def Submission_task( submission ):
    pass