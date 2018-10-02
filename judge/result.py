from enum import Enum, unique
from utils.decorators import classproperty

class _meta:

    __slots__ = (
        'full',
        'alias',
        'color',
        'detail',
        '_field'
    )

    def __init__(self, ** kw):
        for _ in kw:
            setattr( self , _ , kw[_] )
        self._field = [x for x in kw]
    
    def __str__(self):            
        return f'<JudgeResult:{ self.alias }>'
    
    def __repr__(self):
        return f'<JudgeResult:{ self.alias }>'

    @property
    def attribute(self):
        return {x: getattr(self, x) for x in self._field}

@unique
class JudgeResult( Enum ):

    _PD = _meta(
        full = 'Pending',
        alias = 'PD',
        color = 'info',
        detail = 'Judger is too busy to judge your solution. Just be kindly patient to waiting a moment.',
    )

    _PR = _meta(
        full = 'Preparing',
        alias = 'PR',
        color = 'info',
        detail = 'Judger has fetched your solution, now is preparing test data.',
    )

    _AC = _meta(
        full = 'Accepted',
        alias = 'AC',
        color = 'success',
        detail = 'Your solution has produced exactly right output.',
    )

    _RN = _meta(
        full = 'Running',
        alias = 'RN',
        color = 'info',
        detail = 'The program of your solution is running on the judger.',
    )

    _CE = _meta(
        full = 'Compile Error',
        alias = 'CE',
        color = 'warning',
        detail = 'Your solution cannot be compiled into any program that executed by the system.',
    )

    _WA = _meta(
        full = 'Wrong Answer',
        alias = 'WA',
        color = 'error',
        detail = 'Your solution has not produced the desired output for the input given by system.',
    )

    _RE = _meta(
        full = 'Runtime Error',
        alias = 'RE',
        color = 'error',
        detail = 'Your solution has caused an unhandled exception during execution.',
    )

    _TLE = _meta(
        full = 'Time Limit Exceeded',
        alias = 'TLE',
        color = 'error',
        detail = 'Your solution has run for longer time than permitted time limit.',
    )

    _OLE = _meta(
        full = 'Output Limit Exceeded',
        alias = 'OLE',
        color = 'error',
        detail = 'Your solution has produced overmuch output.',
    )

    _MLE = _meta(
        full = 'Memory Limit Exceeded',
        alias = 'MLE',
        color = 'error',
        detail = 'Your solution has consumed more memory than permitted memory limit.',
    )

    _JE = _meta(
        full = 'Judger Error',
        alias = 'JE',
        color = 'warning',
        detail = 'Some unexpected errors occur in judger.',
    )

    @classproperty
    def PD( cls ):
        return cls._PD.value
    
    @classproperty
    def PR( cls ):
        return cls._PR.value
    
    @classproperty
    def AC( cls ):
        return cls._AC.value

    @classproperty
    def RN( cls ):
        return cls._RN.value
    
    @classproperty
    def CE( cls ):
        return cls._CE.value
    
    @classproperty
    def WA( cls ):
        return cls._WA.value

    @classproperty
    def RE( cls ):
        return cls._RE.value

    @classproperty
    def TLE( cls ):
        return cls._TLE.value

    @classproperty
    def OLE( cls ):
        return cls._OLE.value

    @classproperty
    def MLE( cls ):
        return cls._MLE.value
    
    @classproperty
    def JE( cls ):
        return cls._JE.value

    @classmethod
    def value_of( cls , value ):
        for each in cls:
            if each.value.full == value:
                return each.value
        return None

    @classmethod
    def all( cls ):
        return [ each.value for each in cls ]