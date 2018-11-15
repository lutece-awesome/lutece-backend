from __future__ import absolute_import, unicode_literals

from celery import shared_task

from submission.util import Modify_submission_status


@shared_task(name='Judger.task')
def apply_submission(submission):
    pass


@shared_task(name='Judger.result')
def Submission_result(report):
    Modify_submission_status(**report)
