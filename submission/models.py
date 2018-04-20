from django.db import models

# Create your models here.

class Submission(models.Model):
    submission_id = models.AutoField(primary_key=True, db_index=True)
    language = models.CharField(max_length = 64)
    problem_id = models.PositiveIntegerField(default=1)
    judge_status = models.CharField(max_length = 64)
    code = models.CharField(max_length=65535 , blank = True )
