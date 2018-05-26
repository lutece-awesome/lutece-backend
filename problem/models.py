from django.db import models
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify


class Problem(models.Model):
    problem_id = models.AutoField(primary_key=True, db_index=True)
    title = models.CharField(
        max_length=256, db_index=True, default='Default Title', unique = True )
    content = MarkdownxField( blank = True )
    standard_input = MarkdownxField( blank = True )
    standard_output = MarkdownxField( blank = True )
    constraints = MarkdownxField( blank = True )
    resource = models.CharField(max_length=256, blank=True)
    note = models.TextField( blank = True )
    time_limit = models.PositiveIntegerField(default=2000)
    memory_limit = models.PositiveIntegerField(default=128)
    checker = models.CharField( max_length = 256 , default = 'wcmp' )
    visible = models.BooleanField(default = False )

    def __str__(self):
        return self.title
    
    @property
    def content_markdown(self):
        return markdownify( self.content )
    
    @property
    def standard_input_markdown(self):
        return markdownify( self.standard_input )
    
    @property
    def standard_output_markdown(self):
        return markdownify( self.standard_output )
    
    @property
    def constraints_markdown(self):
        return markdownify( self.constraints )

    class Meta:
        ordering = ['problem_id']
        permissions = (
            ('view_all' , 'Can view all problems'),
            ('download_problem_data' , 'Can download test data' ),
        )


class Sample(models.Model):
    sample_id = models.AutoField(primary_key=True, db_index=True)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    input_content = models.CharField( max_length = 512, null = True )
    output_content = models.CharField( max_length = 512, null = True )

    def __str__(self):
        return str(self.sample_id)
