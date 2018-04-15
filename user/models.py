from django.db import models
from django.contrib.auth.models import AbstractUser
from json import dumps
from django.http import HttpResponse

class User(AbstractUser):
    display_name = models.CharField(max_length=128)

    def __str__(self):
        return self.username


def login_required_ajax( function ):
    def wrapper( * argv , ** kw ):
        try:
            if argv[0].user.is_authenticated == False:
                return HttpResponse( dumps( { 'error_msg' : 'Please log in first.' } ) , content_type = 'application/json' )
        except:
            return HttpResponse(dumps({'error_msg': 'Unknown error.'}), content_type='application/json')
        return function( * argv , ** kw )
    return wrapper

