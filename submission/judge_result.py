from user.models import User
from .models import Submission
from re import compile, search

class Judge_info:

    colour = {
        'Waiting': 'grey',
        'Preparing' : 'grey',
        'Accepted' : '#32CD32',
        'Running' : 'black',
        'Compile Error' : 'orange',
        'Wrong Answer' : '#EE2C2C',
        'Runtime Error' : '#CD4F39',
        'Time Limit Exceeded' : '#6495ED' ,
        'Output Limit Exceeded' : '#B03060',
        'Memory Limit Exceeded' : '#CD69C9',
        'Judger Error' : 'red'}

    WT = ( compile( '^Waiting$' ) , 'Waiting' )
    PR = ( compile( '^Preparing$' ) , 'Preparing' )
    AC = ( compile( '^Accepted$' ) , 'Accepted' )
    RN = ( compile( '^Running.*$' ) , 'Running' )
    CE = ( compile( '^Compile Error$' ) , 'Compile Error' )
    WA = ( compile( '^Wrong Answer.*$' ) , 'Wrong Answer' )
    RE = ( compile( '^Runtime Error.*$' ) , 'Runtime Error' )
    TLE = ( compile( '^Time Limit Exceeded.*$' ) , 'Time Limit Exceeded' )
    OLE = ( compile( '^Output Limit Exceeded.*$' ) , 'Output Limit Exceeded' )
    MLE = ( compile( '^Memory Limit Exceeded.*$' ) , 'Memory Limit Exceeded' )
    JE = ( compile( '^Judger Error$' ) , 'Judger Error' )
    
    _fields = ( WT , PR , AC , RN , CE , WA , RE , TLE , OLE , MLE , JE )

    user_detail_fields = ( AC , CE , WA , RE , TLE , OLE , MLE )


def get_index( judge_status ):
    for x in Judge_info._fields:
        if x[0].search( judge_status ) is not None:
            return True , x[1]
    return False , None

def gen_base( fields ):
    return { x[1]:0 for x in fields }