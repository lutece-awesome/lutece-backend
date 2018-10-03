from django.db import models
from judge.models import JudgeResult
from user.models import User
from django.utils import timezone
from problem.models import Problem
from submission.basesubmission.constant import MAX_LANGUAGE_LENGTH
from judge.language import Language

class AbstractSubmission( models.Model ):

    class Meta:
        abstract = True

    result = models.OneToOneField( JudgeResult , on_delete = models.CASCADE )
    problem = models.ForeignKey( Problem , on_delete = models.SET_NULL , null = True )
    user = models.ForeignKey( User , on_delete = models.SET_NULL , null = True )
    create_time = models.DateTimeField( default = timezone.now )
    _language = models.CharField( choices = ( ( each.full , each.full ) for each in Language.all() ) , max_length = MAX_LANGUAGE_LENGTH , db_index = True )

    @property
    def language( self , * args , ** kwargs ):
        return JudgeResult.value_of( self._language )