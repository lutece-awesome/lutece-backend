from .models import Submission, Judgeinfo
from . import JudgeQueue
from annoying.functions import get_object_or_None
from .util import get_update_dict


def Modify_submission_status( ** report ):
    submission = report[ 'submission' ]
    case = report[ 'case' ]
    result = report[ 'result' ]
    complete = report[ 'complete' ]
    if result == 'Running':
        Submission.objects.filter( submission_id = submission ).update( judge_status = 'Running on test ' + str( case ) )
    else:
        sub = Submission.objects.get( submission_id = submission )
        Judgeinfo(
            submission = sub,
            ** get_update_dict( report )).save()
        if complete == True:
            Submission.objects.filter( submission_id = submission ).update( judge_status = result , completed = True )


def push_submission( submission ):
    JudgeQueue.task.put( submission.get_push_dict() )

def read_modify_status():
    while True:
        s = JudgeQueue.result.get( block = True )
        Modify_submission_status( ** s )

def init_push_waiting_submission():
    try:
        f = Submission.objects.filter( judge_status = 'Waiting' )
        for _ in f:
            push_submission( _ )
    except Exception as e:
        print( '- Init push waiting submission failed:' , str( e ) )
    print( '- Init push waiting submission completed,' , str( len( f ) ) + '(s) waiting submissions.' )