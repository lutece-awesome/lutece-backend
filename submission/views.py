from django.shortcuts import render
from django.http import HttpResponse
from annoying.functions import get_object_or_None
from json import dumps
# Create your views here.


def submit_solution(request):
    status = {
        'submission_id' : -1
    }
    try:
        if request.method == 'POST':
            problemid = request.POST.get( 'problemid' )
            code = request.POST.get( 'code' )
            if problemid == None or code == None:
                raise ValueError( "Some solution info missed." )
    finally:
        return HttpResponse( dumps( status ) , content_type = 'application/json' )