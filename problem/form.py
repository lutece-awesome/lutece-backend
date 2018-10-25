from django import forms
from annoying.functions import get_object_or_None
from problem.baseproblem.models import AbstractProblem
from problem.baseproblem.form import AbstractProblemForm
from problem.limitation.form import LimitationForm
from problem.sample.form import SampleForm

class UpdateProblemForm( AbstractProblemForm, LimitationForm, SampleForm ):
    slug = forms.CharField( required = True )

    def clean( self , * args , ** kwargs ):
        cleaned_data = super().clean()
        slug = cleaned_data.get( 'slug' )
        if not get_object_or_None( AbstractProblem , slug = slug ):
            self.add_error( 'slug' , 'Unknown problem for such slug.' )
        return cleaned_data

class CreateProblemForm( AbstractProblemForm , LimitationForm, SampleForm ):
    pass