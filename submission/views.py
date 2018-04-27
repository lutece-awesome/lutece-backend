from django.shortcuts import render
from django.http import HttpResponse,Http404
from annoying.functions import get_object_or_None
from user.models import login_required_ajax
from json import dumps
from django.conf import settings
from .models import Submission, validator_fetch_judge
from problem.models import Problem
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from user.models import User
from django.forms.models import model_to_dict
# Create your views here.

@login_required_ajax
def submit_solution(request):
    status = {
        'submission_id' : -1
    }
    try:
        if request.method == 'POST':
            problemid = request.POST.get( 'problemid' )
            code = request.POST.get( 'code' )
            lang = request.POST.get( 'language' )
            if problemid == None or code == None or lang == None:
                raise ValueError( "Some solution info missed." )
            if len( code ) > settings.MAX_SOURCECORE_LENGTH:
                raise ValueError( "Length of source code is too long." )
            if lang not in settings.SUPPORT_LANGUAGE_LIST:
                raise ValueError( "Unknown language."  )
            s = Submission(
                language = lang,
                user = request.user,
                problem = Problem.objects.get( problem_id = problemid ),
                judge_status = 'Waiting',
                code = code
            )
            s.save()
            status[ 'submission_id' ] = s.submission_id
    finally:
        return HttpResponse( dumps( status ) , content_type = 'application/json' )

def get_status_list(request , page):
    statuslist = Submission.objects.all()
    paginator = Paginator(statuslist, settings.PER_PAGE_COUNT)
    page = min( max( 1 , page ) , paginator.num_pages )
    status = paginator.get_page(page)
    return render(request, 'status/status_list.html', {
        'statuslist': status,
        'max_page': paginator.num_pages,
        'page_list' : range( max( 1 , page - settings.PER_PAGINATOR_COUNT ) , min( page + settings.PER_PAGINATOR_COUNT , paginator.num_pages + 1 ) )
    })

@validator_fetch_judge
def fetch_waiting_submission(request):
    fetch_status = {
        'status' : False,
    }
    try:
        s = Submission.objects.raw( 'SELECT submission_id, MAX( submission_id ) from submission_Submission where judge_status == \'Waiting\'' )[0]
        if s != None:
            s = model_to_dict( s , fields = Submission.Judge.field )
            fetch_status = { **s , ** fetch_status }
            Submission.objects.filter( submission_id = fetch_status['submission_id'] ).update( judge_status = 'Preparing' )
            fetch_status['status'] = True
    finally:
        return HttpResponse( dumps( fetch_status ) , content_type = 'application/json' )

@validator_fetch_judge
def Modify_submission_status(request):
    submission_id = request.POST.get( 'submission_id' )
    print( submission_id )

def get_status_detail(request , submission_id):
    f = Submission.objects.get( submission_id = submission_id )
    pass
