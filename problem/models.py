from django.db import models

class Problem(models.Model):
    problem_id = models.AutoField(primary_key=True, db_index=True)
    title = models.CharField(
        max_length=250, db_index=True, default='Default Title', unique = True )
    content = models.TextField( blank = True )
    standard_input = models.TextField( blank = True )
    standard_output = models.TextField( blank = True )
    constraints = models.TextField( blank = True )
    resource = models.CharField(max_length=250, blank=True)
    note = models.TextField( blank = True )
    time_limit = models.PositiveIntegerField(default=2000)
    memory_limit = models.PositiveIntegerField(default=128)
    checker = models.CharField( max_length = 256 , default = 'wcmp' )
    visible = models.BooleanField( default = False )
    submit = models.IntegerField( default = 0 )
    accept = models.IntegerField( default = 0 )

    def __str__(self):
        return self.title
    class Meta:
        ordering = ['problem_id']
        permissions = (
            ('view_all' , 'Can view all problems'),
            ('download_data' , 'Can download test data' ),
        )


class ContestProblem( models.Model ):
    problem = models.ForeignKey( Problem , on_delete = models.CASCADE , db_index = True )

class Sample(models.Model):
    sample_id = models.AutoField(primary_key=True, db_index=True)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    input_content = models.CharField( max_length = 512, null = True )
    output_content = models.CharField( max_length = 512, null = True )

    def __str__(self):
        return str(self.sample_id)
