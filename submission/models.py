from django.db import models
from submission.basesubmission.models import AbstractSubmission
from submission.constant import MAX_CODE_LENGTH
from submission.attachinfo.models import AbstractAttachInfo
from judge.case.models import AbstractCase


class SubmissionAttachInfo( AbstractAttachInfo ):
    cases_count = models.IntegerField( default =  0 )
    time_cost = models.IntegerField( default = 0 )
    memory_cost = models.IntegerField( default = 0 )


class Submission( AbstractSubmission ):
    code = models.CharField( max_length = MAX_CODE_LENGTH , blank = True )
    attach_info = models.OneToOneField( SubmissionAttachInfo , on_delete = models.CASCADE )


class SubmissionCase( AbstractCase ):
    submission = models.ForeignKey( Submission , on_delete = models.SET_NULL , null = True )