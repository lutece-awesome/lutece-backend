from django.shortcuts import render
from .models import Discussion
from django.http import Http404, HttpResponse
from user.decorators import login_required_ajax
from json import dumps
from annoying.functions import get_object_or_None
from django.contrib.auth.decorators import permission_required

@permission_required('discussion.change_visibility')
def discussion_change_visibility(request):
    status = {
        'status': False,
        'errlist': []}
    err = status['errlist']
    try:
        if request.method == 'POST':
            discussionid = request.POST.get('discussionid')
            visibility = request.POST.get('visibility')
            discussion = get_object_or_None(
                Discussion, pk=discussionid)
            if not discussion:
                raise ValueError('Permission Denied')
            discussion.visibility = visibility
            discussion.save()
            status['status'] = True
    except Exception as e:
        print(str(e))
    finally:
        return HttpResponse(dumps(status), content_type='application/json')