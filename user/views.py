from django.shortcuts import render
from .models import User
from django.http import HttpResponse, QueryDict
from django.contrib.auth import authenticate, login, logout
from json import dumps
from .user_signup.pwd_checker import get_password_strength
from .user_signup.email_checker import get_email_report
from .user_signup.usrname_checker import get_username_strength
from annoying.functions import get_object_or_None

def user_login(request):
    status = {
        'login_status': False
    }
    try:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            if username == None or password == None:
                raise ValueError("username or password do not exist")
            login_user = get_object_or_None( User , username = username )
            if login_user == None:
                raise ValueError("user not exist")
            if login_user.check_password(password):
                login(request, login_user)
                status['login_status'] = True
    finally:
        return HttpResponse(dumps(status), content_type='application/json')


def user_logout(request):
    status = {
        'logout_status': True
    }
    logout(request)
    return HttpResponse(dumps(status), content_type='application/json')


def user_signup(request):
    status = {
        'signup_status': False,
        'error_msg': []
    }
    errormsg_list = status['error_msg']
    try:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            email = request.POST.get('email')
            displayname = request.POST.get('displayname')
            if username == None or password == None or email == None or displayname == None:
                raise ValueError( "Some sign up info do not exist." )
            # Check username
            if len( username ) > 0:
                login_user = get_object_or_None( User,
                    username = username)
                if login_user != None:
                    errormsg_list.append('Username already exists.')
                else:
                    usr_report = get_username_strength( username )
                    if len( usr_report ) > 0:
                        errormsg_list.append( usr_report )
            else:
                errormsg_list.append( 'Username can not be empty.' )
            # Check password
            if len( password ) > 0:
                pwd_check_report = get_password_strength( password )
                for _ in pwd_check_report:
                    errormsg_list.append( _ )
            else:
                errormsg_list.append( 'Password can not be empty.' )
            # Check email
            if len( email ) > 0:
                login_user = get_object_or_None( User,
                    email = email)
                if login_user != None:
                    errormsg_list.append('Email already exists.')
                else:
                    email_report = get_email_report( email )
                    if( len( email_report ) > 0 ):
                        errormsg_list.append( email_report )
            else:
                errormsg_list.append( 'Email can not be empty.' )
            # Check displayname
            if len( displayname ) == 0:
                errormsg_list.append( 'Displayname can not be empty.' )
            elif len( displayname ) > 128:
                errormsg_list.append( 'The length of displayname too long.' )                
            # Check error_msg
            if len( errormsg_list ) == 0:
                new_user = User(
                    username = username,
                    email = email,
                    display_name = displayname
                )
                new_user.set_password( password )
                status['signup_status'] = True
                new_user.save()
                login(request,new_user)
    finally:
        return HttpResponse( dumps( status ) , content_type = 'application/json' )
