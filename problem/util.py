from submission.models import Submission
from problem.models import Problem
from django.http import Http404
from django.db import connection


def get_user_problem_analysis( user , problem ):
    if Submission.objects.filter( user = user , problem = problem , judge_status = 'Accepted' ).count() > 0:
        return 2
    elif Submission.objects.filter( user = user , problem = problem ).count() > 0:
        return 1
    return 0

def get_problem_analysis( problem ):
    s = Submission.objects.filter( problem = problem ).order_by('submission_id')
    ac_user = set()
    _all = 0
    for x in s:
        if x.user.pk in ac_user:
            continue
        _all += 1
        if x.judge_status == 'Accepted':
            ac_user.add( x.user.pk )
    return ( len( ac_user ) , _all )

def check_visible_permission_or_404( user , problem ):
    if not user.has_perm( 'problem.view_all' ) and problem.visible is False:
        raise Http404( 'Permission Denied' )

def InsSubmittimes( pk ):
    if not isinstance( pk , int ):
        return
    with connection.cursor() as cursor:
        cursor.execute( 'UPDATE problem_Problem SET submit = submit + 1 where problem_id = {pk}'.format( pk = pk ) )

def InsAccepttimes( pk ):
    print( 'ready to update' )
    if not isinstance( pk , int ):
        return
    with connection.cursor() as cursor:
        cursor.execute( 'UPDATE problem_Problem SET accept = accept + 1 where problem_id = {pk}'.format( pk = pk ) )
