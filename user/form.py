from django import forms
from user.models import User
from annoying.functions import get_object_or_None


class UserSignupForm( forms.Form ):
    username = forms.CharField( required = True , max_length = 16 , min_length = 4 )
    password = forms.CharField( required = True , max_length = 20 , min_length = 6 )
    email = forms.EmailField( required = True )
    displayname = forms.CharField( required = True , max_length = 12 )

    def clean( self ):
        from re import compile, search
        cleaned_data = super().clean()
        email = cleaned_data.get( 'email' )
        username = cleaned_data.get( 'username' )
        password = cleaned_data.get( 'password' )
        displayname = cleaned_data.get( 'displayname' )
        if username and get_object_or_None( User , username = username ) is not None:
            self.add_error( 'username' , 'Username already exists.' )
        if password and compile( '[a-z]' ).search( password ) is None:
            self.add_error( 'password' , 'Password should contain at least one lowercase letter.' )
        if password and compile( '[A-Z]' ).search( password ) is None:
            self.add_error( 'password' , 'Password should contain at least one uppercase letter.' )
        if email and get_object_or_None( User , email = email ) is not None:
            self.add_error( 'email' , 'Email already exists.' )
        if displayname and get_object_or_None( User , display_name = displayname ) is not None:
            self.add_error( 'displayname' , 'Display name already exists.' )

class UserinfoForm( forms.Form ):
    about = forms.CharField( required = False , max_length = 256 )
    school = forms.CharField( required = False , max_length = 60 )
    company = forms.CharField( required = False , max_length = 32 )
    location = forms.CharField( required = False , max_length = 32 )
    displayname = forms.CharField( required = True , max_length = 16 )

    def _clean( self , PreDisplayname ):
        cleaned_data = super().clean()
        displayname = cleaned_data.get( 'displayname' )
        if displayname and displayname != PreDisplayname and get_object_or_None( User , display_name = displayname ) is not None:
            self.add_error( 'displayname' , 'Display name already exists.' )
            return False
        return True

