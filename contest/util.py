


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
    if datetime.now() >= contest.start_time and contest.visible is False and not user.has_perm( 'contest.view_all' ):
        return False
    return True

def check_contest_submit_code( contest , user , err ):
    from datetime import datetime
    if datetime.now() < contest.start_time and not user.has_perm( 'contest.view_all'):
        err.append( 'Contest has not yet started' )
    elif datetime.now() > contest.end_time and not user.has_perm( 'contest.view_all'):
        err.append( 'Contest has ended' )

def get_contest_analysis( contest ):
    from submission.judge_result import Judge_result, get_judge_result
    from submission.models import Submission
    pos_hashtable = { x.problem : i for i , x in enumerate(contest.contestproblem_set.all()) }
    analysis = [ [0 , 0] for x in range( len( pos_hashtable ) ) ]
    solved_user = [ set() for x in range( len( pos_hashtable ) ) ]
    sub_all = Submission.objects.filter( contest = contest ).order_by( 'pk' )
    for each in sub_all:
        user = each.user
        if user.has_perm( 'contest.view_all' ):
            continue
        _id = each.problem.pk
        if _id in pos_hashtable:
            _id = pos_hashtable[_id]
            se = get_judge_result( each.judge_status )
            if se is Judge_result.AC and user in solved_user[_id]:
                continue
            analysis[_id][1] += 1
            if se is Judge_result.AC:
                analysis[_id][0] += 1
                solved_user[_id].add( user )
    return analysis

def get_user_contest_problem_analysis( user , problem ):
    from submission.models import Submission
    from submission.judge_result import Judge_result
    if Submission.objects.filter( user = user , problem = problem , judge_status = Judge_result.AC.value.full ).count() > 0:
        return True
    return False