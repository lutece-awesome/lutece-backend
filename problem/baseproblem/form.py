from django import forms
from problem.baseproblem.constant import MAX_TITLE_LENGTH, MAX_CONTENT_LENGTH, MAX_RESOURCES_LENGTH, MAX_CONSTRAINTS_LENGTH, MAX_NOTE_LENGTH
from annoying.functions import get_object_or_None
from problem.baseproblem.models import AbstractProblem

class AbstractProblemForm( forms.Form ):
    title = forms.CharField( required = True , max_length = MAX_TITLE_LENGTH )
    content = forms.CharField( required = True , max_length = MAX_CONTENT_LENGTH )
    resouces = forms.CharField( required  = True , max_length = MAX_RESOURCES_LENGTH )
    constraints = models.CharField( required = True , max_length = MAX_CONSTRAINTS_LENGTH )
    note = models.CharField( required = True , max_length = MAX_NOTE_LENGTH )

    def clean( self , * args , ** kwargs ):
        cleaned_data = super().clean()
        title = cleaned_data.get( 'title' )
        if not get_object_or_None( AbstractProblem , title = title ):
            self.add_error( 'title' , 'Title already existed.' )
        return cleaned_data