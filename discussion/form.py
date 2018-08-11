from django import forms
from annoying.functions import get_object_or_None
from .models import Discussion as AbstractDiscussion

class ReplyDiscussionForm( forms.Form ):
    content = forms.CharField( required = True , max_length = 1024 )
    parent = forms.IntegerField( required = True )

    def clean( self ):
        cleaned_data = super().clean()
        parent = cleaned_data.get( 'parent' )
        if get_object_or_None( AbstractDiscussion , pk = parent ) is None:
            self.add_error( 'parent' , 'Unknown reply discussion' )