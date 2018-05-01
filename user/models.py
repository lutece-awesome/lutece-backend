from django.db import models
from django.contrib.auth.models import AbstractUser , Permission
from json import dumps
from django.http import HttpResponse


class Group:

    normal_user = 'normal_user'
    normal_admin = 'normal_admin'

    class Meta:
        normal_user = []
        normal_admin = ['add_problem' , 'change_problem' , 'view_all_submission' , 'download_problem_data' ]


class User(AbstractUser):
    display_name = models.CharField(max_length=128)

    def __str__(self):
        return self.username
    
    def set_group( self , group ):
        for _ in getattr( Group.Meta , group ):
            self.user_permissions.add( Permission.objects.get( codename = _ ) )
