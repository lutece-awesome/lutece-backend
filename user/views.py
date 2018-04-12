from django.shortcuts import render
from .models import user
from django.http import HttpResponse , QueryDict
from django.core import serializers

# Create your views here.


def user_login(request):
    status = {
        'login_status:' : True
    }
    if request.method == 'POST':
        login_user = user.objects.get( username = request.POST['username'] )
        if login_user == None:
            status['login_status'] = False
    return HttpResponse( serializers.serialize( 'json' , status ) , content_type = 'application/json' )