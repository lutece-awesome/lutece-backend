from django.db import models
from judge.models import JudgeResult
from user.models import User
from django.utils import timezone
from problem.baseproblem.models import AbstractProblem
from submission.basesubmission.constant import MAX_CODE_LENGTH

class AbstractSubmission( models.Model ):

    class Meta:
        abstract = True

    result = models.OneToOneField( JudgeResult , on_delete = models.CASCADE )
    problem = models.ForeignKey( AbstractProblem , on_delete = models.SET_NULL )
    user = models.ForeignKey( User , on_delete = models.SET_NULL , null = True )
    create_time = models.DateTimeField( default = timezone.now )