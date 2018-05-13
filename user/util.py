from submission.models import Submission
from submission.judge_result import get_judge_result, Judge_result, Query_field

def get_user_report( user ):
    _all = Submission.objects.filter( user = user )
    if not user.has_perm( 'problem.view_all' ):
        _all = _all.filter( problem__visible = True )
    _all = _all.order_by( 'pk' )
    analysis = dict()
    solved = set()
    tried = set()
    for sub in _all:
        prob = sub.problem.pk
        result = get_judge_result( sub.judge_status )
        if result not in Query_field.basic_field.value:
            continue
        tried.add( prob )
        if result not in analysis:
            analysis[result] = 0
        if prob not in solved:
            analysis[result] += 1
        if result == Judge_result.AC:
            solved.add( prob )
    result = list()
    for each in tried:
        if each in solved:
            result.append( ( each , True ) )
        else:
            result.append( ( each , False ) )
    result.sort()
    return { 'analysis': analysis , 'result' : result }

def get_recently( user , number ):
    s = Submission.objects.filter( user = user )
    if not user.has_perm( 'problem.view_all' ):
        s = s.filter( problem__visible = True )
    return list( s[:number] )

def get_search_url():
    return '/user/search'

def build_detail_url( user_pk ):
    return '/user/detail/' + str( user_pk )