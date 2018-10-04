from django.db import models
from django_extensions.db.models import AutoSlugField
from problem.baseproblem.constant import MAX_TITLE_LENGTH, MAX_CONTENT_LENGTH, MAX_RESOURCES_LENGTH, MAX_CONSTRAINTS_LENGTH, MAX_NOTE_LENGTH, MAX_STANDARD_INPUT_LENGTH, MAX_STANDARD_OUTPUT_LENGTH

class AbstractProblem( models.Model ):

    class Meta:
        abstract = True

    title = models.CharField( max_length = MAX_TITLE_LENGTH , db_index = True )
    content = models.CharField( max_length = MAX_CONTENT_LENGTH , blank = True )
    resources = models.CharField( max_length = MAX_RESOURCES_LENGTH , blank = True )
    constraints = models.CharField( max_length = MAX_CONSTRAINTS_LENGTH , blank = True )
    standard_input = models.CharField( max_length = MAX_STANDARD_INPUT_LENGTH , blank = True )
    standard_output = models.CharField( max_length = MAX_STANDARD_OUTPUT_LENGTH , blank = True )
    note = models.CharField( max_length = MAX_NOTE_LENGTH , blank = True )
    slug = AutoSlugField( populate_from = 'title' , overwrite = True )
    disable = models.BooleanField( default = False )

    def __str__( self ):
        return self.title

    def save( self , * args , ** kwargs ):
        super().save( * args , ** kwargs )
