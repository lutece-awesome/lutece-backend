from django.shortcuts import get_object_or_404,render
from django.http import Http404
from django.http import HttpResponse
from problem.models import problem
from Config import config

# Create your views here.

def problemView( request , problemId ):
    prob = get_object_or_404( problem , problemId = problemId )
    context = { 'prob' : prob.toDict() }
    return render( request , 'problem/problemView.html' , context )


def problemList( request , page ):
    p = problem.objects.raw( 'SELECT problemId , title , tryNumber, solvedNumber FROM problem_problem WHERE problemId BETWEEN {rangel} and {ranger} ORDER BY problemId ASC'.format(
        rangel = ( page - 1 ) * config.perPagecount + 1,
        ranger = page * config.perPagecount
    ))
    return render( request , 'problem/problemList.html' , { 'problist' : p } )
