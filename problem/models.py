from django.db import models


class Problem(models.Model):
    problem_id = models.AutoField(primary_key=True, db_index=True)
    title = models.CharField(
        max_length=256, db_index=True, default='Default Title')
    content = models.TextField( blank=True )
    standard_input = models.TextField( blank = True)
    standard_output = models.TextField( blank = True)
    constraints = models.TextField( blank=True )
    sample_explanation = models.TextField(max_length=1024, blank=True)
    resource = models.CharField(max_length=256, blank=True)
    time_limit = models.PositiveIntegerField(default=2000)
    memory_limit = models.PositiveIntegerField(default=128)
    solved_number = models.PositiveIntegerField(default=0, editable=False)
    try_number = models.PositiveIntegerField(default=0, editable=False)
    checker = models.CharField( max_length = 256 , default = 'wcmp' )
    visible = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['problem_id']
        permissions = (
            ('download_data' , 'Can download test data' ),
        )


class Sample(models.Model):
    sample_id = models.AutoField(primary_key=True, db_index=True)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    input_content = models.TextField( null = True )
    output_content = models.TextField( null = True )

    def __str__(self):
        return str(self.sample_id)
