from django.db import models
from judge.result import JudgeResult
from judge.constant import MAX_RESULT_LENGTH


class JudgeResult( models.Model ):
    _result = models.CharField( choices = ( each.full for each in JudgeResult.all() )  , max_length = MAX_RESULT_LENGTH , db_index = True )
    time_cost = models.IntegerField( default = 0 )
    memory_cost = models.IntegerField( default = 0 )

    @property
    def result( self , * args , ** kwargs ):
        return JudgeResult.value_of( _result )
    