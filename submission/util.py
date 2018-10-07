from submission.models import Submission, SubmissionCase
from judge.result import JudgeResult
from problem.models import Problem
from json import dumps
from django.apps import apps


def Modify_submission_status(** report):
    '''
        Update the status of target submission.
    '''
    result = report['result']
    submission = report['submission']
    name = f'SubmissionDetail-{submission}'
    send_data = dict()
    if 'complete' in report and report['complete'] is True:
        send_data['completed'] = report['complete']
    sub = Submission.objects.get( pk = submission )
    if result == JudgeResult.RN.full or result == JudgeResult.PR.full:
        sub.result._result = result
        sub.result.save()
        send_data['result'] = result
    elif 'judgererror_msg' in report:
        sub.result.done = True
        sub.result.error_info = report['judgererror_msg']
        sub.result._result = result
        sub.result.save()
        send_data['result'] = result
        send_data['judgererror_msg'] = report['judgererror_msg']
    elif 'compileerror_msg' in report:
        sub.result.done = True
        sub.result.compile_info = report['compileerror_msg']
        sub.result._result = result
        sub.result.save()
        send_data['result'] = result
        send_data['compileerror_msg'] = report['compileerror_msg']
    else:
        case = report['case']
        complete = report['complete']
        sub = Submission.objects.get(pk=submission)
        s = SubmissionCase(
            submission = sub,
            _result = report.get( 'result' ),
            time_cost = report.get( 'time_cost' ),
            memory_cost = report.get( 'memory_cost' ),
            case = report.get( 'case' ),
        )
        s.save()
        send_data['judge'] = [s.get_websocket_field()]
        sub.attach_info.time_cost = max(sub.attach_info.time_cost, int(s.time_cost))
        sub.attach_info.memory_cost = max(sub.attach_info.memory_cost, int(s.memory_cost))
        sub.attach_info.save()
        if complete == True:
            sub.result._result = result
            sub.result.done = True
            sub.result.save()
            if JudgeResult.value_of(result) is JudgeResult.AC:
                Problem.objects.get( pk = sub.problem.pk ).ins_accept_times()
            from user.util import update_user_solve
            update_user_solve( sub.user , sub.problem , True if JudgeResult.value_of( result ) is JudgeResult.AC else False )
            send_data['result'] = result
    if apps.is_installed("channels"):
        from channels.layers import get_channel_layer
        from asgiref.sync import async_to_sync
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            name, {"type": "update_result", 'data': send_data})