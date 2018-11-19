from django.apps import apps

from judge.result import JudgeResult
from problem.models import Problem
from submission.consumers import UpdatingData, CaseData
from submission.models import Submission, SubmissionCase


def Modify_submission_status(**report):
    '''
        Update the status of target submission.
    '''
    result = report['result']
    submission = report['submission']
    name = f'SubmissionDetail-{submission}'
    send_data = UpdatingData()
    sub = Submission.objects.get(pk=submission)
    compile_info = report.get('compileerror_msg')
    error_info = report.get('judgererror_msg')
    if result == JudgeResult.RN.full or result == JudgeResult.PR.full:
        sub.result._result = result
        sub.result.save()
        send_data.result = result
    elif error_info:
        sub.result.done = True
        sub.result.error_info = error_info
        sub.result._result = result
        sub.result.save()
        send_data.result = result
        send_data.error_info = error_info
    elif compile_info:
        sub.result.done = True
        sub.result.compile_info = compile_info
        sub.result._result = result
        sub.result.save()
        send_data.result = result
        send_data.compile_info = compile_info
    else:
        complete = report['complete']
        sub = Submission.objects.get(pk=submission)
        s = SubmissionCase(
            submission=sub,
            _result=report.get('result'),
            time_cost=report.get('time_cost'),
            memory_cost=report.get('memory_cost'),
            case=report.get('case'),
        )
        s.save()
        send_data.case_list = [CaseData(
            result=s.result.full,
            time_cost=s.time_cost,
            memory_cost=s.memory_cost,
            case=s.case
        )]
        sub.attach_info.time_cost = max(sub.attach_info.time_cost, int(s.time_cost))
        sub.attach_info.memory_cost = max(sub.attach_info.memory_cost, int(s.memory_cost))
        sub.attach_info.save()
        if complete:
            sub.result._result = result
            sub.result.done = True
            sub.result.save()
            if JudgeResult.value_of(result) is JudgeResult.AC:
                Problem.objects.get(pk=sub.problem.pk).ins_accept_times()
            from user.util import update_user_solve
            update_user_solve(sub.user, sub.problem, True if JudgeResult.value_of(result) is JudgeResult.AC else False)
            sub.user.refresh_solve()
            send_data.result = result
    if apps.is_installed("channels"):
        from channels.layers import get_channel_layer
        from asgiref.sync import async_to_sync
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            name,
            {
                "type": "update_result",
                'data': send_data.serialization()
            }
        )
