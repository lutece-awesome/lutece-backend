from django.shortcuts import get_object_or_404,render
from django.http import Http404
from django.http import HttpResponse
from Problem.models import Problem
from Config import config

# Create your views here.

def problemView( request , problemId ):
    prob = get_object_or_404( Problem , problemId = problemId )
    context = { 'prob' : prob.toDict() }
    return render( request , 'Problem/problemView.html' , context )


def problemList( request , page ):
    p = Problem.objects.raw( 'SELECT problemId , title , tryNumber, solvedNumber FROM Problem_problem WHERE problemId BETWEEN {rangel} and {ranger} ORDER BY problemId ASC'.format(
        rangel = ( page - 1 ) * config.perPagecount + 1,
        ranger = page * config.perPagecount
    ))
    return render( request , 'Problem/problemList.html' , { 'problist' : p } )