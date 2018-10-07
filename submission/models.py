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
    code = models.TextField( max_length = MAX_CODE_LENGTH , blank = True )
    attach_info = models.OneToOneField( SubmissionAttachInfo , on_delete = models.CASCADE )

    def __str__( self ):
    	return f'<Submission:{self.pk}>'
    
    def get_judge_field( self ):
        return {
            'submission_id' : self.pk,
            'language' : self.language.full,
            'code' : self.code,
            'problem' : self.problem.pk,
            'time_limit' : self.problem.limitation.time_limit,
            'memory_limit' : self.problem.limitation.time_limit,
            'checker' : self.problem.checker.full
        }


class SubmissionCase( AbstractCase ):
    submission = models.ForeignKey( Submission , on_delete = models.SET_NULL , null = True )\

    def get_websocket_field( self ):
        return {
            'result' : self.result.full,
            'time_cost' : self.time_cost,
            'memory_cost' : self.memory_cost,
            'case' : self.case
        }