from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from json import dumps
# Create your views here.


@login_required
def create( request ):
    user = request.user
    title = request.POST.get( 'title' )
    content = request.POST.get( 'content' )
    vote = int(request.POST.get( 'vote' )