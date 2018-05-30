from __future__ import absolute_import, unicode_literals
from celery import shared_task
from time import sleep
from .util import Modify_submission_status


@shared_task( name = 'Judger.task' )
def Submission_task( submission ):
    pass

@shared_task( name = 'Judger.result' )
def Submission_result( report ):
    Modify_submission_status( ** report )