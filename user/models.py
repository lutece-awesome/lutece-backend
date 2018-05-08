from django.db import models
from django.contrib.auth.models import AbstractUser , Permission
from json import dumps
from django.http import HttpResponse
from annoying.functions import get_object_or_None
from problem.models import Problem

class Group:

    normal_user = 'normal_user'
    normal_admin = 'normal_admin'

    class Meta:
        normal_user = []
        normal_admin = ['add_problem' , 'change_problem' , 'view_all_submission' , 'download_problem_data' ]


class User(AbstractUser):
    display_name = models.CharField(max_length=16)
    group = models.CharField( max_length = 64 , default = Group.normal_user )

    def __str__(self):
        return self.username
        
    def set_group( self , group ):
        for _ in getattr( Group.Meta , group ):
            self.user_permissions.add( Permission.objects.get( codename = _ ) )

    def save( self , * args , ** kwargs ):
        super( User , self ).save()
        if Userinfo.objects.get( user = self ) == None:
            Userinfo( user = self ) .save()

class Userinfo(models.Model):
    user = models.OneToOneField( User , on_delete = models.CASCADE , primary_key = True )
    school = models.CharField( max_length = 128 , blank = True )
    company = models.CharField( max_length = 128 , blank = True )
    location = models.CharField( max_length = 128 , blank = True )
    about = models.CharField( max_length = 256 , blank = True ) # tell others how awesome you are

    def __str__( self ):
        return self.user.username