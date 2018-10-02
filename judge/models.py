from django.db import models
from judge.result import JudgeResult
from judge.constant import MAX_RESULT_LENGTH, MAX_COMPILE_LENGTH, MAX_ERROR_LENGTH


class JudgeResult( models.Model ):
    _result = models.CharField( choices = ( ( each.full , each.detail ) for each in JudgeResult.all() ) , max_length = MAX_RESULT_LENGTH , db_index = True )
    compile_info = models.CharField( max_length = MAX_COMPILE_LENGTH )
    error_info = models.CharField( max_length = MAX_ERROR_LENGTH )

    @property
    def result( self , * args , ** kwargs ):
        return JudgeResult.value_of( self._result )
    