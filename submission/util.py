from .models import Submission, Judgeinfo
from .judge_result import Judge_result
from problem.util import InsAccepttimes
from json import dumps
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

def Modify_submission_status( ** report ):
    '''
        Update the status of target submission
    '''
    result = report[ 'result' ]
    submission = report[ 'submission' ]
    name = 'StatusDetail_%d' % submission
    if result == 'Running' or result == 'Preparing':
        Submission.objects.filter( pk = submission ).update( judge_status = result )
    elif 'judgererror_msg' in report:
        Submission.objects.filter( pk = submission ).update( completed = True , judgererror_msg = report[ 'judgererror_msg' ] , judge_status = result )
    elif 'compileerror_msg' in report:
        Submission.objects.filter( pk = submission ).update( completed = True , compileerror_msg = report[ 'compileerror_msg' ] , judge_status = result )
    else:
        case = report[ 'case' ]
        complete = report[ 'complete' ]
        sub = Submission.objects.get( pk = submission )
        s = Judgeinfo(
            submission = sub,
            ** get_update_dict( report ))
        s.save()
        if complete == True:
            Submission.objects.filter( pk = submission ).update( judge_status = result , completed = True )
            if Judge_result.get_judge_result( result ) is Judge_result.AC:
                InsAccepttimes( sub.problem.pk )
            from user.util import Modify_user_tried_solved
            Modify_user_tried_solved( sub.user )
        
        # async_to_sync(channel_layer.group_send)( name , {"type": "update_result" , 'data' : construct_websocketdata(
        #     result = result,
        #     judge = [{
        #         'timecost' : s.time_cost,
        #         'memorycost' : s.memory_cost,
        #         'result': s.result,
        #         'case': s.case
        #     }]
        # ) })

def get_update_dict( dic ):
    '''
        return dict of update field filter
    '''
    L = []
    t = dic
    for _ in t:
        if _ not in Submission.Judge.update_field:
            L.append( _ )
    for _ in L:
        t.pop( _ )
    return t


def construct_websocketdata( result , ** extra ):
    return dumps( {**{
        'result' : result,
    } , ** extra } )