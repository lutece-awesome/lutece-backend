from django.db import models
from sample.constant import MAX_INPUT_LENGTH, MAX_OUTPUT_LENGTH

class AbstractSample( models.Model ):
    input_content = models.CharField( max_length = MAX_INPUT_LENGTH , blank = True )
    output_content = models.CharField( max_length = MAX_OUTPUT_LENGTH , blank = True )

    def __str__( self ):
        return str( self.pk )