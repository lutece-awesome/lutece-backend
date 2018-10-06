from django.db import models
from judge.result import JudgeResult as JudgeResultService
from judge.constant import MAX_RESULT_LENGTH

class AbstractCase( models.Model ):

    class Meta:
        abstract = True

    time_cost = models.IntegerField( default = 0 )
    memory_cost = models.IntegerField( default = 0 )
    case = models.IntegerField( default = 0 )
    _result = models.CharField( choices = ( ( each.full , each.detail ) for each in JudgeResultService.all() ) , max_length = MAX_RESULT_LENGTH , db_index = True )

    @property
    def result( self , * args , ** kwargs ):
    	return JudgeResultService.value_of( self._result )