from submission.models import Submission
from submission.judge_result import gen_base, get_index
from submission.judge_result import Judge_info

def get_report( user ):
    s = [ ( x.pk , x.problem.pk , x.judge_status ) for x in Submission.objects.filter( user = user ) ]
    base = gen_base( Judge_info.user_detail_fields )
    analysis = {}
    s.sort()
    for x in s:
        st , _id = get_index( x[2] )
        if st == False:
            continue
        if x[1] not in analysis:
            analysis[x[1]] = base.copy()
        if analysis[x[1]][Judge_info.AC[1]] > 0:
            continue
        analysis[x[1]][_id] += 1
    solved = 0 
    tried = 0
    summary = base.copy()
    for x in analysis:
        for y in analysis[x]:
            summary[y] += analysis[x][y]
        if analysis[x][Judge_info.AC[1]] > 0:
            solved += 1
        else:
            tried += 0
    return { ** analysis , ** { 'solved' : solved , 'tried' : tried , 'summary' : summary } }