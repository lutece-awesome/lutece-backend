from django.shortcuts import render , get_object_or_404
from django.http import HttpResponse,Http404
from annoying.functions import get_object_or_None
from user.models import User
from user.decorators import login_required_ajax
from json import dumps
from django.conf import settings
import Lutece.config as config
from .models import Submission, Judgeinfo
from problem.models import Problem
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from utils.paginator_menu import get_range as page_range
from data_server.util import get_case_number
from .judge_result import get_judge_result_list, Judge_result
from problem.util import check_visible_permission_or_404, InsSubmittimes
from utils.language import get_language, get_language_list
from .tasks import Submission_task
# Create your views here.

@login_required_ajax
def submit_solution(request):
    status = {
        'status' : False,
        'errlist' : []}
    err = status['errlist']
    try:
        if request.method == 'POST':
            from contest.models import Contest
            problemid = request.POST.get( 'problemid' )
            code = request.POST.get( 'code' )
            lang = request.POST.get( 'language' )
            contest = get_object_or_None( Contest , pk = request.POST.get( 'contest' ) )
            problem = Problem.objects.get( pk = problemid )
            if contest is None:
                if not problem.visible and not request.user.has_perm( 'problem.view_all' ):
                    raise ValueError( "Permission Denied" )
            else:
                # to do , contest submission auth
                pass
            if len( code ) > config.MAX_SOURCECORE_LENGTH:
                err.append( 'The length of source code is too long, limit is ' + str( config.MAX_SOURCECORE_LENGTH ) )
                raise ValueError( "Length of source code is too long." )
            s = Submission(
                language = lang,
                user = request.user,
                problem = problem,
                case_number = get_case_number( problemid ),
                judge_status = Judge_result.PD.value.full,
                contest = contest,
                code = code)
            s.save()
            Submission_task.apply_async( args = (s.get_push_dict() ,) , queue = settings.TASK_QUEUE )
            InsSubmittimes( int(problemid) ) # would not be injection
            status[ 'pk' ] = s.pk
            status['status'] = True
    finally:
        return HttpResponse( dumps( status ) , content_type = 'application/json' )

def get_status_list(request , page):
    statuslist = Submission.objects.filter( contest = None )
    display_name = request.GET.get( 'display_name' )
    title = request.GET.get( 'title' )
    verdict = request.GET.get( 'verdict' )
    lang = request.GET.get( 'lang' )
    try:
        if not request.user.has_perm( 'problem.view_all' ):
            statuslist = statuslist.filter( problem__visible = True )
        if display_name is not None:
            statuslist = statuslist.filter( user = User.objects.get( display_name = display_name ) )
        if title is not None:
            statuslist = statuslist.filter( problem = Problem.objects.get( title = title ) )
        if verdict is not None:
            statuslist = statuslist.filter( judge_status = verdict )
        if lang is not None:
            statuslist = statuslist.filter( language = lang )
    except:
        statuslist = Submission.objects.none()
    paginator = Paginator(statuslist, config.PER_PAGE_COUNT)
    page = min( max( 1 , page ) , paginator.num_pages )
    status = paginator.get_page(page)
    return render(request, 'status/status_list.html', {
        'querystring': request.META['QUERY_STRING'],
        'meta': request.GET.dict(),
        'statuslist': status,
        'currentpage' : page,
        'judge_result_list' : get_judge_result_list(),
        'language_list' : get_language_list(),
        'max_page': paginator.num_pages,
        'page_list' : page_range( page , paginator.num_pages )})


def get_status_detail(request , submission_id):
    target = get_object_or_404( Submission , pk = submission_id )
    check_visible_permission_or_404( user = request.user , problem = target.problem )
    return render( request , 'status/status_detail.html' , {
        'status' : target })
        
def get_status_detail_json( request , submission_id ):
    try:
        status = {
            'status' : False,
            'detail' : []}
        sub = submission = Submission.objects.get( pk = submission_id )
        s = Judgeinfo.objects.filter( submission = sub )
        if not request.user.has_perm( 'problem.view_all' ) and not sub.problem.visible:
            raise RuntimeError( 'Permission Denied' )
        status['detail'] = [ ( ( x.case , x.result ,  x.time_cost , x.memory_cost ) ) for x in s ]
        status['status'] = True
    finally:
        return HttpResponse( dumps( status ) , content_type = 'application/json' )

def get_activity_json( request , user_pk ):
    user = User.objects.get( pk = user_pk )
    import datetime, time
    now = datetime.datetime.now()
    start_date =  now - datetime.timedelta(days=366)
    s = Submission.objects.filter( user = user , submit_time__date__gt = start_date )
    return HttpResponse( dumps( { int(time.mktime(x.submit_time.timetuple())) : 1 for x in s } ) , content_type = 'application/json' )


def get_submission_code( request , pk ):
    status = {
        'status' : False,
        'prism' : '',
        'code' : ''}
    from utils.language import get_prism
    try:
        sub = Submission.objects.get( pk = pk )
        if sub.user == request.user or request.user.has_perm( 'submission.view_all' ):
            status['code'] = sub.code
            status['status'] = True
            status['prism'] = get_prism( sub.language )
        else:
            code = 'Permission Denied'
    finally:
        return HttpResponse( dumps( status ) , content_type = 'application/json' )