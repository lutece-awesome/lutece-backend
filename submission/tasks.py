from .models import Submission, Judgeinfo
from .task_queue import task, result
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
        if get_object_or_None( Judgeinfo , submission = sub , case = case ) == None:
            Judgeinfo(
                submission = sub,
                case = case).save()
        Judgeinfo.objects.filter( submission = submission , case = case ).update( ** get_update_dict( report ) )
        if complete == True:
            msg = result
            if result != 'Accepted' and result != 'Compile Error' and result != 'Judger Error':
                msg += ' on test ' + str( case )
            Submission.objects.filter( submission_id = submission ).update( judge_status = msg )

def push_submission( submission ):
    task.put( submission.get_push_dict() )

def read_modify_status():
    while True:
        s = result.get( block = True )
        Modify_submission_status( ** s )

def init_push_waiting_submission():
    try:
        f = Submission.objects.filter( judge_status = 'Waiting' )
        for _ in f:
            push_submission( _ )
    except Exception as e:
        print( '- Init push waitting submission failed:' , str( e ) )
    print( '- Init push waitting submission completed,' , str( len( f ) ) + '(s) waitting submissions.' )