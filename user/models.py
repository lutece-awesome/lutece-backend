from django.db import models
from django.contrib.auth.models import AbstractUser
from user.attachinfo.models import AttachInfo
from problem.models import Problem

class User( AbstractUser ):
    attach_info = models.OneToOneField( AttachInfo , on_delete = models.CASCADE )
    solved = models.IntegerField( default = 0 )
    tried = models.IntegerField( default = 0 )
    
    def __str__(self):
        return f'<User:{self.username}>'

class Solve( models.Model ):
    user = models.ForeignKey( User , on_delete = models.SET_NULL , null = True )
    problem = models.ForeignKey( Problem , on_delete = models.SET_NULL , null = True )
    status = models.BooleanField( default = False )