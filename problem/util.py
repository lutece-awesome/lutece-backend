from submission.models import Submission


def get_user_problem_analysis( user , problem ):
    if len( Submission.objects.filter( user = user , problem = problem , judge_status = 'Accepted' ) ) > 0:
        return 2
    elif len( Submission.objects.filter( user = user , problem = problem ) ) > 0:
        return 1
    return 0

def get_problem_analys( problem ):
    return ( len( { x.user for x in Submission.objects.filter( problem = problem , judge_status = 'Accepted' ) } ),
             len( { x.user for x in Submission.objects.filter( problem = problem ) } ))