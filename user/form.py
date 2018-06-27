from django import forms
from user.models import User

class UserSignupForm( forms.Form ):
    email = forms.EmailField( required = True )
    username = forms.CharField( required = True , max_length = 16 , min_length = 4 )
    password = forms.CharField( required = True , max_length = 20 , min_length = 6 )

    def clean( self ):
        email = self.cleaned_data( 'email' )