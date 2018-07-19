from django import forms
from Lutece.config import MAX_SOURCECORE_LENGTH
from problem.models import Problem
from utils.language import Language
from annoying.functions import get_object_or_None

class SubmitSolutionForm( forms.Form ):
    problemslug = forms.CharField( required = True )
    code = forms.CharField( required = True , max_length = MAX_SOURCECORE_LENGTH , min_length = 1 )
    language = forms.CharField( required = True )

    def clean( self ):
        cleaned_data = super().clean()
        problemslug = cleaned_data.get( 'problemslug' )
        code = cleaned_data.get( 'code' )
        language = Language.get_language( cleaned_data.get( 'language' ) )
        s = get_object_or_None( Problem , slug = problemslug )
        if problemslug and s is None:
            self.add_error( 'problemslug' , 'Problem not exists.' )
        if language is None:
            self.add_error( 'language' , 'Unknown language' )
