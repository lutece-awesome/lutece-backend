from enum import Enum, unique

class _meta:
    __slots__ = (
        'full',
        'icon',
        'color',
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

class ContestStatus( Enum ):

    PENDING = _meta(
        full = 'Pending',
        icon = 'coffee icon',
        color = 'grey'
    )
    RUNNING = _meta(
        full = 'Running',
        icon = 'notched circle loading icon',
        color = '#2185d0'
    )
    COMPLETE = _meta(
        full = 'Completed',
        icon = 'check icon',
        color = 'green'
    )

def get_contest_status( start_time , end_time ):
    from datetime import datetime
    now = datetime.now()
    if start_time > now:
        return ContestStatus.PENDING
    elif end_time <= now:
        return ContestStatus.COMPLETE
    return ContestStatus.RUNNING
