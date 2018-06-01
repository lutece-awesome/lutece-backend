from django.db import models
from problem.models import Problem

# Create your models here.

class Contest( models.Model ):
    contest_id = models.AutoField( primary_key = True , db_index = True )
    title = models.CharField( max_length = 32 , blank = True )
    contest_type = models.CharField( max_length = 32 , blank = True )
    password = models.CharField( max_length = 32 , blank = True )
    note = models.TextField( blank = True )
    visible = models.BooleanField(default = False )
    start_time = models.DateTimeField( null = False )
    end_time = models.DateField( null = False )

    class Meta:
        ordering = ['-contest_id']
        permissions = (
            ('view_all' , 'Can view all contest' ),
        )


class ContestProblem( models.Model ):
    problem = models.ForeignKey( Problem , on_delete = models.CASCADE , db_index = True )