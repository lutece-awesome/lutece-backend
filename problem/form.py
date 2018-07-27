from django import forms
from annoying.functions import get_object_or_None
from .models import Problem


class UpdateProblemForm( forms.Form ):
    title = forms.CharField( required = True , max_length = 64)
    resource = forms.CharField( max_length = 128 )
    time_limit = forms.IntegerField( max_value = 60000 , min_value = 1 )
    memory_limit = forms.IntegerField( max_value = 1024 , min_value = 1 )
    slug = forms.CharField( required = True )

    def clean( self ):
        cleaned_data = super().clean()
        title = cleaned_data.get( 'title' )
        slug = cleaned_data.get( 'slug' )
        s = get_object_or_None( Problem ,title = title )
        if s is not None and s.slug != slug:
            self.add_error( 'title' , 'Title already existed' )