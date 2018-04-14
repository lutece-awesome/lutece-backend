from django.db import models

# Create your models here.

class Submission(models.Model):
    submission_id = models.AutoField(primary_key=True, db_index=True)
    language = models.CharField(max_length = 64)
    judge_status = models.CharField(max_length = 256)
