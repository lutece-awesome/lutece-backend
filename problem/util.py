from submission.models import Submission


def get_user_problem_analysis( user , problem ):
    if len( Submission.objects.filter( user = user , problem = problem , judge_status = 'Accepted' ) ) > 0:
        return 2
    elif len( Submission.objects.filter( user = user , problem = problem ) ) > 0:
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

def get_search_url():
    return '/problem/search'


def build_detail_url( prob_pk ):
    return '/problem/detail/' + str( prob_pk )