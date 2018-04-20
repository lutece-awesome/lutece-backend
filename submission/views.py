from django.shortcuts import render
from django.http import HttpResponse
from annoying.functions import get_object_or_None
from user.models import login_required_ajax
from json import dumps
from django.conf import settings
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
    finally:
        return HttpResponse( dumps( status ) , content_type = 'application/json' )