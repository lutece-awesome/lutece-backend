from django.shortcuts import render
from .models import User
from django.http import HttpResponse, QueryDict
from django.contrib.auth import authenticate, login, logout
from json import dumps


def user_login(request):
    status = {
        'login_status': False
    }
    try:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            if username == None or password == None:
                raise ValueError("username or password not exist")
            login_user = User.objects.get(
                username=request.POST.get('username'))
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
