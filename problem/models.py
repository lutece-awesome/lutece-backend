from django.db import models


class Problem(models.Model):
    problem_id = models.AutoField(primary_key=True, db_index=True)
    title = models.CharField(
        max_length=256, db_index=True, default='Default Title')
    content = models.CharField(max_length=58000, blank=True)
    constraints = models.CharField(max_length=1024, blank=True)
    sample_explanation = models.CharField(max_length=1024, blank=True)
    resource = models.CharField(max_length=256, blank=True)
    time_limit = models.PositiveIntegerField(default=2000)
    memory_limit = models.PositiveIntegerField(default=128)
    solved_number = models.PositiveIntegerField(default=0, editable=False)
    try_number = models.PositiveIntegerField(default=0, editable=False)
    special_judge = models.BooleanField(default=False)
    visible = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['problem_id']


class Sample(models.Model):
    sample_id = models.AutoField(primary_key=True, db_index=True)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    input_content = models.CharField( max_length = 256 )
    output_content = models.CharField( max_length = 256 )

    def __str__(self):
        return str(self.sample_id)
