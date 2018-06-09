from django.db import models

import django.utils.timezone as timezone
from user.models import User

# Create your models here.

class Contest( models.Model ):
    contest_id = models.AutoField( primary_key = True , db_index = True )
    title = models.CharField( max_length = 64 , blank = True , unique = True )
    contest_type = models.CharField( max_length = 32 , blank = True )
    password = models.CharField( max_length = 32 , blank = True )
    note = models.TextField( blank = True )
    visible = models.BooleanField(default = False )
    register = models.BooleanField( default = False )
    start_time = models.DateTimeField( null = False , default = timezone.now  )
    end_time = models.DateTimeField( null = False , default = timezone.now )

    class Meta:
        ordering = ['-contest_id']
        permissions = (
            ('view_all' , 'Can view all contest' ),
        )
class ContestInvitedUser( models.Model ):
    user = models.ForeignKey( User , on_delete = models.CASCADE , db_index = True )

class ContestProblem( models.Model ):
    contest = models.ForeignKey( Contest , on_delete = models.CASCADE , db_index = True )
    problem = models.IntegerField( blank = False )