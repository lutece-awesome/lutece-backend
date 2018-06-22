from django.db import models
from django.contrib.auth.models import AbstractUser , Permission
from json import dumps
from django.http import HttpResponse
from annoying.functions import get_object_or_None
from .group import Group



class User(AbstractUser):
    display_name = models.CharField(max_length = 16 , unique = True )
    group = models.CharField( max_length = 64 , default = Group.NORMAL_USER.value.full )
    email = models.EmailField( blank=True , unique = True )
    school = models.CharField( max_length = 60 , blank = True )
    company = models.CharField( max_length = 32 , blank = True )
    location = models.CharField( max_length = 32 , blank = True )
    about = models.CharField( max_length = 256 , blank = True , default = '这个人很懒,什么都没有写' )
    tried = models.IntegerField( default = 0 )
    solved = models.IntegerField( default = 0 )
    show = models.BooleanField( default = True )

    def __str__(self):
        return self.username

    def set_group( self , group ):
        self.user_permissions.clear()
        for _ in group.value.permission:
            _.set_permission( self )
        self.group = group.value.full
        self.show = group.value.show_in_userlist
        self.save()

    class Meta:
        permissions = (
            ('set_normal_user' , 'Can set normal_user' ),
            ('set_normal_admin' , 'Can set normal_admin' ),
            ('set_super_admin' , 'Can set super_admin' ),
        )

class Followrelation(models.Model):
    target = models.OneToOneField( User , on_delete = models.CASCADE , primary_key = True , related_name = 'target' )
    who = models.OneToOneField( User , on_delete = models.CASCADE , db_index = True , related_name = 'who' )