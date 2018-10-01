from django import forms
from annoying.functions import get_object_or_None
from problem.baseproblem.models import AbstractProblem
from problem.baseproblem.form import AbstractProblemForm
from problem.limitation.form import LimitationForm
from problem.sample.form import SampleForm

class UpdateProblemForm( AbstractProblemForm, LimitationForm, SampleForm ):

    def clean( self , * args , ** kwargs ):
        cleaned_data = super().clean()
        title = cleaned_data.get( 'title' )
        if title and not get_object_or_None( AbstractProblem , title = title ):
            self.add_error( 'title' , 'Unknown title for such a problem.' )
        return cleaned_data

class CreateProblemForm( AbstractProblemForm , LimitationForm, SampleForm ):

    def clean( self , * args , ** kwargs ):
        cleaned_data = super().clean()
        title = cleaned_data.get( 'title' )
        if title and get_object_or_None( AbstractProblem , title = title ):
            self.add_error( 'title' , 'Title already existed.' )
        return cleaned_data