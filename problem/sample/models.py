from django.db import models
from problem.sample.constant import MAX_SAMPLE_INPUT_LENGTH, MAX_SAMPLE_OUTPUT_LENGTH

class AbstractSample( models.Model ):
    input_content = models.CharField( max_length = MAX_SAMPLE_INPUT_LENGTH , blank = True )
    output_content = models.CharField( max_length = MAX_SAMPLE_OUTPUT_LENGTH , blank = True )