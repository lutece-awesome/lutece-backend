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
        'Memory Limit Exceeded' : '#EE3B3B',
        'Judger Error' : 'red'}

    WT = ( compile( '^Waiting$' ) , 'Waiting' , 'WT' )
    PR = ( compile( '^Preparing$' ) , 'Preparing' , 'PR' )
    AC = ( compile( '^Accepted$' ) , 'Accepted' , 'AC' )
    RN = ( compile( '^Running.*$' ) , 'Running' , 'RN' )
    CE = ( compile( '^Compile Error$' ) , 'Compile Error' , 'CE' )
    WA = ( compile( '^Wrong Answer.*$' ) , 'Wrong Answer' , 'WA' )
    RE = ( compile( '^Runtime Error.*$' ) , 'Runtime Error' , 'RE' )
    TLE = ( compile( '^Time Limit Exceeded.*$' ) , 'Time Limit Exceeded' , 'TLE' )
    OLE = ( compile( '^Output Limit Exceeded.*$' ) , 'Output Limit Exceeded' , 'OLE' )
    MLE = ( compile( '^Memory Limit Exceeded.*$' ) , 'Memory Limit Exceeded' , 'MLE' )
    JE = ( compile( '^Judger Error$' ) , 'Judger Error' , 'JE' )
    
    _fields = ( WT , PR , AC , RN , CE , WA , RE , TLE , OLE , MLE , JE )

    user_detail_fields = ( AC , CE , WA , RE , TLE , OLE , MLE )


def get_index( judge_status , fields = Judge_info._fields ):
    for x in fields:
        if x[0].search( judge_status ) is not None:
            return True , x[1]
    return False , None

def gen_base( fields ):
    return { x[1]:0 for x in fields }