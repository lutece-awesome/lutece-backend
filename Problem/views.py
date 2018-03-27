from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def problemView( request ):
    return HttpResponse( "This is problem show page" );
