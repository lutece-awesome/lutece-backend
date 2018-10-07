from django.db import models
from user.models import User
from problem.models import Problem

class Solve( models.Model ):
    user = models.ForeignKey( User , on_delete = models.SET_NULL , null = True )
    problem = models.ForeignKey( Problem , on_delete = models.SET_NULL , null = True )
    status = models.BooleanField( default = False )