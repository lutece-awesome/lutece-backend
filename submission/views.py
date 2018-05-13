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
from .tasks import push_submission
from utils.paginator_menu import get_range as page_range
from data_server.util import get_case_number
from .util import prism_name_transfer
from .judge_result import get_judge_result_list
from problem.util import get_search_url as problem_search_url
from user.util import get_search_url as user_search_url
from problem.util import check_visible_permission_or_404
# Create your views here.

@login_required_ajax
def submit_solution(request):
    status = {
        'submission_id' : -1}
    try:
        if request.method == 'POST':
            problemid = request.POST.get( 'problemid' )
            code = request.POST.get( 'code' )
            lang = request.POST.get( 'language' )
            problem = Problem.objects.get( pk = problemid )
            if problemid == None or code == None or lang == None:
                raise ValueError( "Some solution info missed." )
            if not problem.visible and not request.user.has_perm( 'problem.view_all' ):
                raise ValueError( "Permission Denied" )
            if len( code ) > config.MAX_SOURCECORE_LENGTH:
                raise ValueError( "Length of source code is too long." )
            if lang not in config.SUPPORT_LANGUAGE_LIST:
                raise ValueError( "Unknown language."  )
            s = Submission(
                language = lang,
                user = request.user,
                problem = problem,
                case_number = get_case_number( problemid ),
                judge_status = 'Waiting',
                code = code)
            s.save()
            push_submission( s )
            status[ 'submission_id' ] = s.submission_id
    finally:
        return HttpResponse( dumps( status ) , content_type = 'application/json' )


def get_status_list(request , page):
    statuslist = Submission.objects.all()
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
        'language_list' : config.SUPPORT_LANGUAGE_LIST,
        'user_search_url' : user_search_url(),
        'problem_search_url' : problem_search_url(),
        'max_page': paginator.num_pages,
        'page_list' : page_range( page , paginator.num_pages )})


def get_status_detail(request , submission_id):
    target = get_object_or_404( Submission , pk = submission_id )
    check_visible_permission_or_404( user = request.user , problem = target.problem )
    return render( request , 'status/status_detail.html' , {
        'status' : target,
        'prism' : prism_name_transfer( target.language ) })


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
