from django.shortcuts import render
from django.http import HttpResponse,Http404
from django.views.decorators.csrf import csrf_exempt
from annoying.functions import get_object_or_None
from user.models import User
from user.decorators import login_required_ajax
from json import dumps
from django.conf import settings
import Lutece.config as config
from .models import Submission, Judgeinfo
from .decorators import validator_fetch_judge
from .util import get_update_dict
from problem.models import Problem
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
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
            # push_submission(
            #     submission = s.submission_id,
            #     language = lang,
            #     code = code,
            #     time_limit = s.problem.time_limit,
            #     memory_limit = s.problem.memory_limit,
            #     checker = s.problem.checker,
            #     problem = s.problem_id)
            s.save()
            status[ 'submission_id' ] = s.submission_id
    except Exception as e:
        print( str( e ) )
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


# @validator_fetch_judge
# def fetch_waiting_submission(request):
#     fetch_status = {
#         'status' : False,}
#     try:
#         s = Submission.objects.raw( 'SELECT submission_id, MIN( submission_id ) from submission_Submission where judge_status == \'Waiting\'' )[0]
#         if s != None:
#             s.get_problem_field( fetch_status )
#             fetch_status = { ** fetch_status ,  ** model_to_dict( s , fields = Submission.Judge.field ) }
#             Submission.objects.filter( submission_id = fetch_status['submission_id'] ).update( judge_status = 'Preparing' )
#             fetch_status['status'] = True
#     finally:
#         return HttpResponse( dumps( fetch_status ) , content_type = 'application/json' )


@csrf_exempt
@validator_fetch_judge
def Modify_submission_status(request):
    submission = request.POST.get( 'submission' )
    case = request.POST.get( 'case' )
    result = request.POST.get( 'result' )
    complete = request.POST.get( 'complete' )
    if result == 'Running':
        Submission.objects.filter( submission_id = submission ).update( judge_status = 'Running on test ' + str( case ) )
    else:
        sub = Submission.objects.get( submission_id = submission )
        if get_object_or_None( Judgeinfo , submission = sub , case = case ) == None:
            Judgeinfo(
                submission = sub,
                case = case).save()
        Judgeinfo.objects.filter( submission = submission , case = case ).update( ** get_update_dict( request.POST.dict() ) )
        if complete == 'True':
            msg = result
            if result != 'Accepted' and result != 'Compile Error' and result != 'Judger Error':
                msg += ' on test ' + str( case )
            Submission.objects.filter( submission_id = submission ).update( judge_status = msg )
    return HttpResponse( None )


def get_status_detail(request , submission_id):
    f = Submission.objects.get( submission_id = submission_id )
    pass
