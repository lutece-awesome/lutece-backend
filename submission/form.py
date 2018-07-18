from django import forms
from Lutece.config import MAX_SOURCECORE_LENGTH
from problem.models import Problem

class SubmitSolutionForm( forms.Form ):
    problemslug = forms.CharField( required = True )
    code = forms.CharField( required = True , max_length = MAX_SOURCECORE_LENGTH )
    language = forms.CharField( required = True )

    def clean( self ):
        cleaned_data = super().clean()
        problemslug = cleaned_data.get( 'problemslug' )
        code = cleaned_data.get( 'code' )
        language = cleaned_data.get( 'language' )
        s = get_object_or_None( Problem , slug = problemslug )
        if problemslug and s is None:
            self.add_error( 'problemslug' , 'Problem not exists.' )
        