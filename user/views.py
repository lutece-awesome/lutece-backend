from django.shortcuts import render
from user.models import user
from django.http import HttpResponse , QueryDict
from django.contrib.auth import authenticate
from json import dumps

# Create your views here.

def user_login(request):
    status = {
        'login_status' : False
    }
    try:
        if request.method == 'POST':
            username = request.POST.get( 'username' )
            password = request.POST.get( 'password' )
            if username == None or password == None:
                raise ValueError( "username or password not exist" )
            login_user = user.objects.get( username = request.POST.get('username') )
            if login_user == None:
                raise ValueError( "user not exist" )
            if login_user.check_password( password ):
                status['login_status'] = True
    finally:
        return HttpResponse( dumps( status ) , content_type = 'application/json' )