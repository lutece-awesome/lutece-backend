from django.db import models
from django.contrib.auth.models import AbstractUser , Permission
from json import dumps
from django.http import HttpResponse
from annoying.functions import get_object_or_None
from enum import Enum, unique

@unique
class Group( Enum ):

    class _meta:
        __slots__ = (
            'full',
            'display',
            'permission',
            '_field'
        )

        def needdisplay( self ):
            return hasattr( self , 'display' )

        def __init__( self , ** kw ):
            for _ in kw:
                self.__setattr__( _ , kw[_] )
            self._field = [x for x in kw]

        def __str__(self):
            return self.full

        def __repr__(self):
            return str( self.full )
        
        @property
        def attribute(self):
            return { x : getattr( self , x ) for x in self._field }

    NORMAL_USER = _meta(
        full = 'normal_user',
        permission = []
    )

    NORMAL_ADMIN = _meta(
        full = 'normal_admin',
        display = 'Admin',
        permission = ['add_problem' , 'change_problem' , 'view_all_problem' , 'download_data_problem' , 'view_all_submission' , 'view_all_contest' , 'hide_submission_contest']
    )

    SUPER_ADMIN = _meta(
        full = 'super_admin',
        display = 'Super Admin',
        permission = ['add_problem' , 'change_problem' , 'view_all_problem' , 'download_data_problem' , 'view_all_submission' , 'add_contest' , 'change_contest' , 'view_all_contest' , 'hide_submission_contest' , 'set_normal_admin' ],
    )




class User(AbstractUser):
    display_name = models.CharField(max_length = 16 , unique = True )
    group = models.CharField( max_length = 64 , default = Group.NORMAL_USER.value.full )
    email = models.EmailField( blank=True , unique = True )

    def __str__(self):
        return self.username
        
    def set_group( self , group ):
        self.user_permissions.clear()
        for _ in group.value.permission:
            self.user_permissions.add( Permission.objects.get( codename = _ ) )

    def save( self , * args , ** kwargs ):
        super( User , self ).save()
        if get_object_or_None( Userinfo , user = self ) == None:
            Userinfo( user = self ) .save()
    class Meta:
        permissions = (
            ('set_normal_admin' , 'Can set normal_admin' ),
            ('set_super_admin' , 'Can set super_admin' ),
        )

class Userinfo(models.Model):
    user = models.OneToOneField( User , on_delete = models.CASCADE , primary_key = True )
    school = models.CharField( max_length = 60 , blank = True )
    company = models.CharField( max_length = 32 , blank = True )
    location = models.CharField( max_length = 32 , blank = True )
    about = models.CharField( max_length = 256 , blank = True , default = '这个人很懒,什么都没有写' ) # tell others how awesome you are
    tried = models.IntegerField( default = 0 )
    solved = models.IntegerField( default = 0 ) 

    def __str__( self ):
        return self.user.username

class Followrelation(models.Model):
    target = models.OneToOneField( User , on_delete = models.CASCADE , primary_key = True , related_name = 'target' )
    who = models.OneToOneField( User , on_delete = models.CASCADE , db_index = True , related_name = 'who' )