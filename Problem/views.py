from django.shortcuts import render
from django.http import Http404
from django.http import HttpResponse
from Problem.models import Problem

# Create your views here.

def problemView( request , problemId ):
    try:
        prob = Problem.objects.get( problemId = problemId )
    except:
        raise Http404( "Problem %s not found." % problemId )
    return HttpResponse( "This is problem %d." % problemId )