from django import forms
from problem.sample.constant import MAX_SAMPLE_INPUT_LENGTH, MAX_SAMPLE_OUTPUT_LENGTH
from json import loads

class SampleForm( forms.Form ):
    samples = forms.CharField( required = True )
    
    def clean( self , * args , ** kwargs ):
        cleaned_data = super().clean()
        samples = cleaned_data.get( 'samples' )
        sample_arr = loads( samples )
        for each in sample_arr:
            input_content = each.get( 'input_content' )
            output_content = each.get( 'output_content' )
            if len( input_content ) > MAX_SAMPLE_INPUT_LENGTH or len( output_content ) > MAX_SAMPLE_OUTPUT_LENGTH:
                self.add_error( 'samples' , 'The length of sample is too long.' )
                break
        return cleaned_data