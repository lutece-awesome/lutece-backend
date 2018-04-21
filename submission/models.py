from django.db import models
from user.models import User
from problem.models import Problem
import django.utils.timezone as timezone

# Create your models here.

class Submission(models.Model):
    submission_id = models.AutoField(primary_key=True, db_index=True)
    language = models.CharField(max_length = 64)
    problem = models.ForeignKey(Problem,on_delete = models.CASCADE , null = True)
    judge_status = models.CharField(max_length = 64)
    code = models.CharField(max_length=65535 , blank = True )
    submit_time = models.DateTimeField( 'Submit time' , null = True , default = timezone.now )
    user = models.ForeignKey(User,on_delete = models.CASCADE , null = True)