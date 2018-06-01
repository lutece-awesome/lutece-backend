from enum import Enum, unique

class _meta:
    __slots__ = (
        'full',
        'detail',
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


class ContestType( Enum ):
    ICPC = _meta(
        full = 'ACM-ICPC',
        detail = 'ACM-ICPC'
    )
    OI = _meta(
        full = 'OI',
        detail = 'OI Subtask'
    )