from submission.models import Submission
from submission.judge_result import Judge_result, Query_field

def get_user_report( user , has_perm ):
    _all = Submission.objects.filter( user = user )
    if not has_perm:
        _all = _all.filter( problem__visible = True )
    _all = _all.order_by( 'pk' )
    analysis = dict()
    solved = set()
    tried = set()
    for sub in _all:
        prob = sub.problem.pk
        result = Judge_result.get_judge_result( sub.judge_status )
        if result not in Query_field.basic_field.value:
            continue
        tried.add( prob )
        if result not in analysis:
            analysis[result] = 0
        if prob not in solved:
            analysis[result] += 1
        if result is Judge_result.AC:
            solved.add( prob )
    result = list()
    for each in tried:
        if each in solved:
            result.append( ( each , True ) )
        else:
            result.append( ( each , False ) )
    result.sort()
    return { 'analysis': analysis , 'result' : result }

def get_user_solved( user ):
    return Submission.objects.filter( user = user , judge_status = Judge_result.AC.value.full  ).values( 'problem' ).distinct().count()

def get_user_tried( user ):
    return Submission.objects.filter( user = user ).values( 'problem' ).distinct().count()

def Modify_user_tried_solved( user ):
    user.tried = get_user_tried( user )
    user.solved = get_user_solved( user )
    user.save()

def get_recently( user , number , has_perm ):
    s = Submission.objects.filter( user = user )
    if not has_perm:
        s = s.filter( problem__visible = True )
    return list( s[:number] )