from enum import Enum, unique
from utils.decorators import classproperty

class _meta:
    __slots__ = (
        'full',
        'info',
        '_field'
    )

    def __init__( self , ** kw ):
        for _ in kw:
            self.__setattr__( _ , kw[_] )
        self._field = [x for x in kw]

    def __str__(self):
        return f'<Checker:{ self.full }>'

    def __repr__(self):
        return f'<Checker:{ self.full }>'
    
    @property
    def attribute(self):
        return { x : getattr( self , x ) for x in self._field }
        
@unique
class Checker( Enum ):
            
    _WCMP = _meta(
        full = 'wcmp',
        info = 'Compare sequences of tokens',
    )

    _RCMP6 = _meta(
        full = 'rcmp6',
        info = 'Compare two sequences of doubles, max absolute or relative  error = 1E-6',
    )

    _SPJ = _meta(
        full = 'spj',
        info = 'Customized judge program',
    )

    @classproperty
    def WCMP( cls ):
        return cls._WCMP.value

    @classproperty
    def RCMP6( cls ):
        return cls._RCMP6.value
    
    @classproperty
    def SPJ( cls ):
        return cls._SPJ.value

    @classmethod
    def value_of( cls , value ):
        for each in cls:
            if each.value.full == value:
                return each.value
        return None

    @classmethod
    def all( cls ):
        return [ each.value for each in cls ]
