


def auth_user_enter_contest( user , contest ):
    pass


class ContestProblemAnalysis:
    __slots__ = (
        'solved',
        'try_times',
        'penalty',
        'firstblood',
        'first_solve_timedelta',
        '_field'
    )

    def __init__( self , ** kw ):
        for _ in kw:
            self.__setattr__( _ , kw[_] )
        self._field = [x for x in kw]

    def __str__(self):
        return self.attribute

    def __repr__(self):
        return str( self.attribute )
    
    @property
    def attribute(self):
        return { x : getattr( self , x ) for x in self._field }
    
def time_format_hms( s ):
    seconds = s.seconds
    hours = seconds // 3600 + s.days * 24
    seconds = seconds % 3600
    mins = seconds // 60
    seconds = seconds % 60
    last = '%.2d:%.2d:%.2d' % ( hours, mins, seconds )
    return last

def time_format_hm( s ):
    seconds = s.seconds
    hours = seconds // 3600 + s.days * 24
    seconds = seconds % 3600
    mins = seconds // 60
    seconds = seconds % 60
    last = '%.2d:%.2d' % ( hours, mins )
    return last