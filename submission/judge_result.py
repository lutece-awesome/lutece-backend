from re import compile, search
from enum import Enum, unique
from .models import Judgeinfo
class _meta:
    __slots__ = (
        'full',
        'alias',
        'color',
        'regex',
        'detail',
        '_field'
    )

    def __init__( self , ** kw ):
        for _ in kw:
            self.__setattr__( _ , kw[_] )
        self._field = [x for x in kw]

    def __str__(self):
        return self.full

    def __repr__(self):
        return str( self.full )
    
    @property
    def attribute(self):
        return { x : getattr( self , x ) for x in self._field }

@unique
class Judge_result( Enum ):

    PD = _meta(
        full = 'Pending',
        alias = 'PD',
        color = 'info',
        detail = 'Judger is too busy to judge your solution. Just be kindly patient to waiting a moment.',
        regex = compile( '^Pending$' )
    )
    PR = _meta(
        full = 'Preparing',
        alias = 'PR',
        color = 'info',
        detail = 'Judger has fetched your solution, now is preparing test data.',
        regex = compile( '^Preparing$' )
    )
    AC = _meta(
        full = 'Accepted',
        alias = 'AC',
        color = 'success',
        detail = 'Your solution has produced exactly right output.',
        regex = compile( '^Accepted$' )
    )
    RN = _meta(
        full = 'Running',
        alias = 'RN',
        color = 'info',
        detail = 'The program of your solution is running on the judger.',
        regex = compile( '^Running.*$' )
    )
    CE = _meta(
        full = 'Compile Error',
        alias = 'CE',
        color = 'warning',
        detail = 'Your solution cannot be compiled into any program that executed by the system.',
        regex = compile( '^Compile Error$' )
    )
    WA = _meta(
        full = 'Wrong Answer',
        alias = 'WA',
        color = 'error',
        detail = 'Your solution has not produced the desired output for the input given by system.',
        regex = compile( '^Wrong Answer.*$' )
    )
    RE = _meta(
        full = 'Runtime Error',
        alias = 'RE',
        color = 'error',
        detail = 'Your solution has caused an unhandled exception during execution.',
        regex = compile( '^Runtime Error.*$' )
    )
    TLE = _meta(
        full = 'Time Limit Exceeded',
        alias = 'TLE',
        color = 'error',
        detail = 'Your solution has run for longer time than permitted time limit.',
        regex = compile( '^Time Limit Exceeded.*$' )
    )
    OLE = _meta(
        full = 'Output Limit Exceeded',
        alias = 'OLE',
        color = 'error',
        detail = 'Your solution has produced overmuch output.',
        regex = compile( '^Output Limit Exceeded.*$' )    
    )
    MLE = _meta(
        full = 'Memory Limit Exceeded',
        alias = 'MLE',
        color = 'error',
        detail = 'Your solution has consumed more memory than permitted memory limit.',
        regex = compile( '^Memory Limit Exceeded.*$' )    
    )
    JE = _meta(
        full = 'Judger Error',
        alias = 'JE',
        color = 'warning',
        detail = 'Some unexpected errors occur in judger.',
        regex = compile( '^Judger Error$' )  
    )

    @classmethod
    def get_judge_result( cls , result ):
        for each in cls:
            if each.value.regex.search( result ) is not None:
                return each
        return None


class Query_field( Enum ):
    all_fields = ( Judge_result.PD , Judge_result.PR , Judge_result.AC , Judge_result.RN , Judge_result.CE , Judge_result.WA , Judge_result.RE , Judge_result.TLE , Judge_result.OLE , Judge_result.MLE , Judge_result.JE )
    basic_field = ( Judge_result.AC , Judge_result.CE , Judge_result.WA , Judge_result.RE , Judge_result.TLE , Judge_result.OLE , Judge_result.MLE )
    listshow_field = ( Judge_result.AC , Judge_result.WA , Judge_result.RE , Judge_result.TLE , Judge_result.OLE , Judge_result.MLE )
    contest_field = ( Judge_result.AC , Judge_result.WA , Judge_result.RE, Judge_result.TLE , Judge_result.OLE, Judge_result.MLE )
    failedcase_field = ( Judge_result.WA , Judge_result.RE , Judge_result.TLE , Judge_result.OLE , Judge_result.MLE )

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

def get_judge_result_list():
    return list( Judge_result )