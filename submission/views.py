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
from data_server.util import get_case_number
from .util import prism_name_transfer
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
            if problemid == None or code == None or lang == None:
                raise ValueError( "Some solution info missed." )
            if len( code ) > config.MAX_SOURCECORE_LENGTH:
                raise ValueError( "Length of source code is too long." )
            if lang not in config.SUPPORT_LANGUAGE_LIST:
                raise ValueError( "Unknown language."  )
            s = Submission(
                language = lang,
                user = request.user,
                problem = Problem.objects.get( problem_id = problemid ),
                judge_status = 'Waiting',
                code = code)
            s.save()
            push_submission( s )
            status[ 'submission_id' ] = s.submission_id
    finally:
        return HttpResponse( dumps( status ) , content_type = 'application/json' )


def get_status_list(request , page):
    statuslist = Submission.objects.all()
    paginator = Paginator(statuslist, config.PER_PAGE_COUNT)
    page = min( max( 1 , page ) , paginator.num_pages )
    status = paginator.get_page(page)
    return render(request, 'status/status_list.html', {
        'statuslist': status,
        'max_page': paginator.num_pages,
        'page_list' : range( max( 1 , page - config.PER_PAGINATOR_COUNT ) , min( page + config.PER_PAGINATOR_COUNT , paginator.num_pages + 1 ) )})


def get_status_detail(request , submission_id):
    target = get_object_or_404( Submission , pk = submission_id )
    return render( request , 'status/status_detail.html' , {
        'status' : target,
        'case_number' : get_case_number( target.problem.pk ),
        'prism' : prism_name_transfer( target.language ) })


def get_status_detail_json( request , submission_id ):
    try:
        status = {
            'status' : False,
            'detail' : []}
        s = Judgeinfo.objects.filter( submission = Submission.objects.get( pk = submission_id ) )
        status['detail'] = [ ( ( x.case , x.result ,  x.time_cost , x.memory_cost ) ) for x in s ]
        status['status'] = True
    finally:
        return HttpResponse( dumps( status ) , content_type = 'application/json' )