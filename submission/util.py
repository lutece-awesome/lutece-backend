from .models import Submission, Judgeinfo
from .judge_result import Judge_result
from problem.util import InsAccepttimes
from json import dumps


def Modify_submission_status(** report):
    '''
        Update the status of target submission
    '''
    result = report['result']
    submission = report['submission']
    name = 'StatusDetail_%d' % submission
    send_data = dict()
    if 'complete' in report and report['complete'] is True:
        send_data['completed'] = report['complete']
    if result == Judge_result.RN.value.full or result == Judge_result.PR.value.full:
        Submission.objects.filter(pk=submission).update(judge_status=result)
        send_data['result'] = result
    elif 'judgererror_msg' in report:
        Submission.objects.filter(pk=submission).update(
            completed=True, judgererror_msg=report['judgererror_msg'], judge_status=result)
        send_data['result'] = result
        send_data['judgererror_msg'] = report['judgererror_msg']
    elif 'compileerror_msg' in report:
        Submission.objects.filter(pk=submission).update(
            completed=True, compileerror_msg=report['compileerror_msg'], judge_status=result)
        send_data['result'] = result
        send_data['compileerror_msg'] = report['compileerror_msg']
    else:
        case = report['case']
        complete = report['complete']
        sub = Submission.objects.get(pk=submission)
        s = Judgeinfo(
            submission=sub,
            **get_update_dict(report))
        s.save()
        send_data['judge'] = [s.get_websocket_field()]
        sub.time_cost = max(sub.time_cost, int(s.time_cost))
        sub.memory_cost = max(sub.memory_cost, int(s.memory_cost))
        if complete == True:
            sub.judge_status = result
            sub.completed = True
            if Judge_result.get_judge_result(result) is Judge_result.AC:
                InsAccepttimes(sub.problem.pk)
            from user.util import Modify_user_tried_solved
            Modify_user_tried_solved(sub.user)
            send_data['result'] = result
        sub.save()
    try:
        from channels.layers import get_channel_layer
        from asgiref.sync import async_to_sync
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            name, {"type": "update_result", 'data': send_data})            
    except ImportError:
        print('WARNING: fail to import channels.')


def get_update_dict(dic):
    '''
        return dict of update field filter
    '''
    L = []
    t = dic
    for _ in t:
        if _ not in Submission.Judge.update_field:
            L.append(_)
    for _ in L:
        t.pop(_)
    return t
