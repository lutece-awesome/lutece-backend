from .models import User
from submission.models import Submission
from re import compile, search

class Usersolveinfo:

    base = {
        'Accepted' : 0,
        'Compile Error' : 0,
        'Wrong Answer' : 0,
        'Runtime Error' : 0,
        'Time Limit Exceeded' : 0,
        'Output Limit Exceeded' : 0,
        'Memory Limit Exceeded' : 0
    }

    colour = {
        'Accepted' : '#32CD32',
        'Compile Error' : 'orange',
        'Wrong Answer' : '#EE2C2C',
        'Runtime Error' : '#CD4F39',
        'Time Limit Exceeded' : '#6495ED' ,
        'Output Limit Exceeded' : '#B03060' ,
        'Memory Limit Exceeded' : '#CD69C9',
    }

    AC = [ compile( '^Accepted$' ) , 'Accepted' ]
    CE = [ compile( '^Compile Error$' ) , 'Compile Error' ]
    WA = [ compile( '^Wrong Answer.*$' ) , 'Wrong Answer' ]
    RE = [ compile( '^Runtime Error.*$' ) , 'Runtime Error' ]
    TLE = [ compile( '^Time Limit Exceeded.*$' ) , 'Time Limit Exceeded' ]
    OLE = [ compile( '^Output Limit Exceeded.*$' ) , 'Output Limit Exceeded' ]
    MLE = [ compile( '^Memory Limit Exceeded.*$' ) , 'Memory Limit Exceeded' ]
    
    _fields = [ AC , CE , WA , RE , TLE , OLE , MLE ]


def get_index( judge_status ):
    for x in Usersolveinfo._fields:
        if x[0].search( judge_status ) is not None:
            return True , x[1]
    return False , None

def get_report( user ):
    s = [ [ x.pk , x.problem.pk , x.judge_status ]  for x in Submission.objects.filter( user = user ) ]
    analysis = {}
    s.sort()
    # [ pk , problem_pk , judge_status ]
    for x in s:
        st , _id = get_index( x[2] )
        if st == False:
            continue
        if x[1] not in analysis:
            analysis[x[1]] = Usersolveinfo.base.copy()
        if analysis[x[1]]['Accepted'] > 0:
            continue
        analysis[x[1]][_id]  += 1 
    solved = 0 
    tried = 0
    summary = Usersolveinfo.base.copy()
    for x in analysis:
        for y in analysis[x]:
            summary[y] += analysis[x][y]
        if analysis[x]['Accepted'] > 0:
            solved += 1
        else:
            tried += 0
    return { ** analysis , ** { 'solved' : solved , 'tried' : tried , 'summary' : summary } } 