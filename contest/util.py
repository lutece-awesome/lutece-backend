


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


def check_contest_started_or_has_perms( contest , user ):
    from datetime import datetime
    from django.http import Http404
    if datetime.now() < contest.start_time and not user.has_perm( 'contest.view_all'):
        return False
    print( 'run 1' )
    if datetime.now() >= contest.start_time and contest.visible is False and not user.has_perm( 'contest.view_all' ):
        return False
    return True

def check_contest_submit_code( contest , user , err ):
    from datetime import datetime
    if datetime.now() < contest.start_time and not user.has_perm( 'contest.view_all'):
        err.append( 'Contest has not yet started' )
    elif datetime.now() > contest.end_time and not user.has_perm( 'contest.view_all'):
        err.append( 'Contest has ended' )