


def auth_user_enter_contest( user , contest ):
    pass


class ContestProblemAnalysis:
    __slots__ = (
        'solved',
        'try_times',
        'penalty',
        'firstblood',
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