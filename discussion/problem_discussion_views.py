from django.shortcuts import render
from .models import Discussion
from django.http import Http404, HttpResponse
from user.decorators import login_required_ajax
from json import dumps
from annoying.functions import get_object_or_None
from django.contrib.auth.decorators import permission_required


def problem_discussion_show(request, pk):
    from problem.models import Problem
    view_all = request.user and request.user.has_perm('discussion.view_all')
    problem = Problem.objects.get( pk = pk )
    if ( not problem.discussionvisible or not problem.visible ) and not request.user.has_perm('discussion.view_all'):
        raise RuntimeError('Permission Denied')
    discussion = problem.problemdiscussion_set.all()
    return render(request, 'discussion/problem_discussion_content.html', {
        'discussion':  discussion,
        'problem' : problem,
        'view_all': view_all})


@login_required_ajax
def problem_discussion_reply( request , pk ):
    from problem.models import Problem, ProblemDiscussion
    status = {
        'status': False,
        'errlist': []}
    try:
        err = status['errlist']
        problem = Problem.objects.get( pk = pk )
        content = request.POST.get('content')
        if not content:
            err.append('Empty content')
            raise RuntimeError('Empty content')
        elif len( content ) > 200:
            err.append('Content length too long')
            raise RuntimeError('Content length too long')
        if ( not problem.discussionvisible or not problem.visible ) and not request.user.has_perm('discussion.view_all'):
            raise RuntimeError('Permission Denied')
        ProblemDiscussion(
            problem = problem,
            user = request.user,
            content = content ).save()
        status['status'] = True
    finally:
        return HttpResponse(dumps(status), content_type='application/json')

@login_required_ajax
def problem_discussion_change_like_status( request , pk ):
    from problem.models import Problem, ProblemDiscussion
    status = {
        'status': False,
        'errlist': []}
    try:
        err = status['errlist']
        problem = Problem.objects.get( pk = pk )
        content = request.POST.get('content')
        if not content:
            err.append('Empty content')
            raise RuntimeError('Empty content')
        elif len( content ) > 200:
            err.append('Content length too long')
            raise RuntimeError('Content length too long')
        if ( not problem.discussionvisible or not problem.visible ) and not request.user.has_perm('discussion.view_all'):
            raise RuntimeError('Permission Denied')
        ProblemDiscussion(
            problem = problem,
            user = request.user,
            content = content ).save()
        status['status'] = True
    finally:
        return HttpResponse(dumps(status), content_type='application/json')