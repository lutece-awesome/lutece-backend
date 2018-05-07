from django.db import models
from user.models import User
from problem.models import Problem
from django.forms.models import model_to_dict

import django.utils.timezone as timezone
from django.http import Http404

# Create your models here.

class Submission(models.Model):
    submission_id = models.AutoField( primary_key=True , db_index=True )
    language = models.CharField( max_length = 64 )
    problem = models.ForeignKey( Problem,on_delete = models.CASCADE , null = True )
    judge_status = models.CharField( max_length = 64 , db_index = True )
    code = models.CharField( max_length=65535 , blank = True )
    submit_time = models.DateTimeField( 'Submit time' , null = True , default = timezone.now )
    user = models.ForeignKey( User , on_delete = models.CASCADE , null = True )
    completed = models.BooleanField( default = False )

    class Meta:
        ordering = ['-submission_id']
        permissions = (
            ('view_all' , 'Can view all submission' ),
        )

    class Judge:
        field = ['submission_id' , 'language' , 'problem' , 'code' ]
        problem_field = [ 'time_limit' , 'memory_limit' , 'checker' ]
        update_field = [ 'submission' , 'result' , 'time_cost' , 'memory_cost' , 'additional_info' , 'case' ]

    def get_problem_field( self , dic ):
        for _ in self.Judge.problem_field:
            dic[_] = getattr( self.problem , _ )
    
    def get_push_dict( self ):
        dic = {}
        self.get_problem_field( dic )
        return { ** dic , ** model_to_dict( self , fields = self.Judge.field ) }

class Judgeinfo(models.Model):
    judgeinfo_id = models.AutoField(primary_key=True, db_index=True)
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE )
    result = models.CharField( max_length = 64 , default = '' )
    time_cost = models.CharField( max_length = 12 )
    memory_cost = models.CharField( max_length = 12 )
    additional_info = models.CharField( max_length = 512 )
    case = models.SmallIntegerField( null = True , editable = False , db_index = True )

    def __str__(self):
        return str(self.judgeinfo_id)
    
    class Meat:
        ordering = ['case']

