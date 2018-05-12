from re import compile, search
from enum import Enum, unique
from .models import Judgeinfo

class _result:
    __slots__ = (
        'full',
        'alias',
        'color',
        'regex',
        'detail',
        'icon',
        '_field'
    )

    def __init__( self , ** kw ):
        for _ in kw:
            self.__setattr__( _ , kw[_] )
        self._field = kw

    def __str__(self):
        return self.full

    def __repr__(self):
        return str( self.full )
    
    @property
    def attribute(self):
        return self._field

@unique
class Judge_result( Enum ):
    WT = _result(
        full = 'Waiting',
        alias = 'WT',
        color = 'grey',
        detail = 'Judger is too busy to judge your solution. Just be kindly patient to waiting a moment.',
        icon = 'ui coffee icon',
        regex = compile( '^Waiting$' )
    )
    PR = _result(
        full = 'Preparing',
        alias = 'PR',
        color = 'grey',
        icon = 'ui coffee icon',
        detail = 'Judger has fetched your solution, now is preparing test data.',
        regex = compile( '^Preparing$' )
    )
    AC = _result(
        full = 'Accepted',
        alias = 'AC',
        color = '#21ba45',
        icon = 'ui check icon',
        detail = 'Your solution has produced exactly right output.',
        regex = compile( '^Accepted$' )
    )
    RN = _result(
        full = 'Running',
        alias = 'RN',
        color = '#666699',
        icon = 'ui hourglass half icon',
        detail = 'The program of your solution is running on the judger.',
        regex = compile( '^Running.*$' )
    )
    CE = _result(
        full = 'Compile Error',
        alias = 'CE',
        color = 'orange',
        icon = 'ui exclamation icon',
        detail = 'Your solution cannot be compiled into any program that executed by the system.',
        regex = compile( '^Compile Error$' )
    )
    WA = _result(
        full = 'Wrong Answer',
        alias = 'WA',
        color = 'red',
        icon = 'ui times icon',
        detail = 'Your solution has not produced the desired output for the input given by system.',
        regex = compile( '^Wrong Answer.*$' )
    )
    RE = _result(
        full = 'Runtime Error',
        alias = 'RE',
        color = '#CC0033',
        icon = 'ui times icon',
        detail = 'Your solution has caused an unhandled exception during execution.',
        regex = compile( '^Runtime Error.*$' )
    )
    TLE = _result(
        full = 'Time Limit Exceeded',
        alias = 'TLE',
        color = '#6666FF',
        icon = 'ui times icon',
        detail = 'Your solution has run for longer time than permitted time limit.',
        regex = compile( '^Time Limit Exceeded.*$' )
    )
    OLE = _result(
        full = 'Output Limit Exceeded',
        alias = 'OLE',
        color = '#FF0033',
        icon = 'ui times icon',
        detail = 'Your solution has produced overmuch output.',
        regex = compile( '^Output Limit Exceeded.*$' )    
    )
    MLE = _result(
        full = 'Memory Limit Exceeded',
        alias = 'MLE',
        color = '#CC3333',
        icon = 'ui times icon',
        detail = 'Your solution has consumed more memory than permitted memory limit.',
        regex = compile( '^Memory Limit Exceeded.*$' )    
    )
    JE = _result(
        full = 'Judger Error',
        alias = 'JE',
        color = '#EE2C2C',
        icon = 'ui exclamation circle icon',
        detail = 'Some unexpected errors occur in judger.',
        regex = compile( '^Judger Error$' )  
    )

@unique
class Query_field( Enum ):
    all_fields = ( Judge_result.WT , Judge_result.PR , Judge_result.AC , Judge_result.RN , Judge_result.CE , Judge_result.WA , Judge_result.RE , Judge_result.TLE , Judge_result.OLE , Judge_result.MLE , Judge_result.JE )
    basic_field = ( Judge_result.AC , Judge_result.CE , Judge_result.WA , Judge_result.RE , Judge_result.TLE , Judge_result.OLE , Judge_result.MLE )
    listshow_field = ( Judge_result.AC , Judge_result.WA , Judge_result.RE , Judge_result.TLE , Judge_result.OLE , Judge_result.MLE )


def get_judge_result( result ):
    for x in Judge_result:
        if x.value.regex.search( result ) is not None:
            return x
    return None

def get_judge_result_color( result ):
    return get_judge_result( result ).value.color

def get_judge_result_icon( result ):
    return get_judge_result( result ).value.icon

def check_judge_result_in_listshow_field( result ):
    return get_judge_result( result ) in Query_field.listshow_field.value

def is_compile_error( result ):
    return get_judge_result( result ) is Judge_result.CE

def is_judger_error( result ):
    return get_judge_result( result )is Judge_result.JE

def get_CE_JE_info( submission ):
    return Judgeinfo.objects.get( submission = submission ).additional_info