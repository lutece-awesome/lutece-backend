from django.shortcuts import get_object_or_404,render
from django.http import Http404
from django.http import HttpResponse
from Problem.models import Problem

# Create your views here.

def problemView( request , problemId ):
    prob = get_object_or_404( Problem , problemId = problemId )
    context = { 'prob' : prob.toDict() }
    return render( request , 'Problem/problemView.html' , context )