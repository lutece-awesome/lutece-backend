from django.shortcuts import render
from django.http import HttpResponse
from annoying.functions import get_object_or_None
from user.models import login_required_ajax
from json import dumps
from django.conf import settings
from .models import Submission
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
                problem_id = problemid,
                judge_status = 'Queuing',
                code = code
            )
            s.save()
            status[ 'submission_id' ] = s.submission_id
    finally:
        return HttpResponse( dumps( status ) , content_type = 'application/json' )