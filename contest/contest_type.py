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
        self._field = [x for x in kw]

    def __str__(self):
        return self.full

    def __repr__(self):
        return str( self.full )
    
    @property
    def attribute(self):
        return { x : getattr( self , x ) for x in self._field }
    
class ContestType( Enum ):
    
    ICPC = _meta(
        full = 'ACM-ICPC',
        detail = 'ACM-ICPC Style'
    )
    # OI = _meta(
    #     full = 'OI( Subtask )',
    #     detail = 'OI Subtask Style'
    # )

def get_contest_type( result ):
    for x in ContestType:
        if x.value.full == result:
            return x
    return None

def get_contest_type_list():
    return list( ContestType )
