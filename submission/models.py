from django.db import models
from user.models import User
from problem.models import Problem
from contest.models import Contest
from django.forms.models import model_to_dict

import django.utils.timezone as timezone
from django.http import Http404
from functools import reduce
# Create your models here.

class Submission(models.Model):
    submission_id = models.AutoField( primary_key=True , db_index=True )
    language = models.CharField( max_length = 64 )
    problem = models.ForeignKey( Problem,on_delete = models.CASCADE , null = True )
    judge_status = models.CharField( max_length = 64 , db_index = True )
    code = models.TextField( blank = True )
    submit_time = models.DateTimeField( 'Submit time' , null = True , default = timezone.now )
    user = models.ForeignKey( User , on_delete = models.CASCADE , null = True , db_index = True )
    completed = models.BooleanField( default = False )
    case_number = models.IntegerField( default = 0 )
    contest = models.ForeignKey( Contest , on_delete = models.CASCADE , null = True , db_index = True )
    judgererror_msg = models.CharField( max_length = 512 , default = '' )
    compileerror_msg = models.CharField( max_length = 512 , default = '' )
    class Meta:
        ordering = ['-submission_id']
        permissions = (
            ('view_all' , 'Can view all submission' ),
        )

    class Judge:
        field = ['submission_id' , 'language' , 'problem' , 'code' ]
        problem_field = [ 'time_limit' , 'memory_limit' , 'checker' ]
        update_field = [ 'result' , 'time_cost' , 'memory_cost' , 'additional_info' , 'case' ]

    def get_problem_field( self , dic ):
        for _ in self.Judge.problem_field:
            dic[_] = getattr( self.problem , _ )
    
    def get_push_dict( self ):
        dic = {}
        self.get_problem_field( dic )
        return { ** dic , ** model_to_dict( self , fields = self.Judge.field ) }

    @property
    def timecost( self ):
        s = Judgeinfo.objects.filter( submission = self )
        return reduce( lambda x , y : max( x , y ) , [ x.time_cost for x in s ] , 0 )

    @property
    def memorycost( self ):
        s = Judgeinfo.objects.filter( submission = self )
        return reduce( lambda x , y : max( x , y ) , [ x.memory_cost for x in s ] , 0 )
        
class Judgeinfo(models.Model):
    judgeinfo_id = models.AutoField(primary_key=True, db_index = True )
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE , db_index = True )
    result = models.CharField( max_length = 64 , default = '' )
    time_cost = models.IntegerField( default = 0 )
    memory_cost = models.IntegerField( default = 0 )
    additional_info = models.CharField( max_length = 512 )
    case = models.SmallIntegerField( null = True , editable = False )

    def __str__(self):
        return str(self.judgeinfo_id)
    class Meat:
        ordering = ['case']