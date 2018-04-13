from django.shortcuts import render
from .models import User
from django.http import HttpResponse, QueryDict
from django.contrib.auth import authenticate, login, logout
from json import dumps
from .password_strength.pwd_checker import get_password_strength


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
            login_user = User.objects.get(
                username=username)
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
    try:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            email = request.POST.get('email')
            displayname = request.POST.get('displayname')
            if username == None or password == None or email == None or displayname == None:
                raise ValueError('some signup info do not exist')
            login_user = User.objects.get(
                username=username)
            if login_user != None:
                status['error_msg'].append('username already exists.')
            login_user = User.objects.get(
                email=email)
            if login_user != None:
                status['error_msg'].append('email already exists.')
            pwd_check_report = get_password_strength(password)
            if len(pwd_check_report) == 0 and len(status['error_msg']) == 0:
                status['signup_status'] = True
            else:
                status['error_msg'].append(pwd_check_report)
    finally:
        return HttpResponse(dumps(status), content_type='application/json')
