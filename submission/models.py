from django.db import models
from user.models import User
from problem.models import Problem
import django.utils.timezone as timezone
from submission.validator import validate_fetch_judge
from django.http import Http404

# Create your models here.

class Submission(models.Model):
    submission_id = models.AutoField(primary_key=True, db_index=True)
    language = models.CharField(max_length = 64)
    problem = models.ForeignKey(Problem,on_delete = models.CASCADE , null = True)
    judge_status = models.CharField(max_length = 64)
    code = models.CharField(max_length=65535 , blank = True )
    submit_time = models.DateTimeField( 'Submit time' , null = True , default = timezone.now )
    user = models.ForeignKey(User,on_delete = models.CASCADE , null = True)
    class Meta:
        ordering = ['-submission_id']

    class Judge:
        field = ['submission_id' , 'language' , 'problem' , 'code' ]


def validator_fetch_judge( function ):
    def wrapper( * argv , ** kw ):
        try:
            if validate_fetch_judge( argv[0] ) == False:
                raise PermissionError()
        except PermissionError:
            raise Http404( 'Permission Denied' )
        except:
            raise Http404( 'Unknown Error' )
        return function( * argv , ** kw )
    return wrapper