from django import forms
from user.models import User
from annoying.functions import get_object_or_None
from user.attachinfo.form import AttachInfoForm
from user.constant import MAX_USERNAME_LENGTH, MIN_USERNAME_LENGTH, MAX_PASSWORD_LENGTH, MIN_PASSWORD_LENGTH

class UserLoginForm( forms.Form ):
    username = forms.CharField( required = True )
    password = forms.CharField( required = True )

    def clean( self ):
        cleaned_data = super().clean()
        username = cleaned_data.get( 'username' )
        password = cleaned_data.get( 'password' )
        usr = get_object_or_None( User , username = username )
        if username and usr is None:
            self.add_error( 'username' , 'Username not exists.' )
        if password and usr and not usr.check_password( password ):
            self.add_error( 'password' , 'Password is wrong.' )
        return cleaned_data

class UserSignupForm( AttachInfoForm ):
    username = forms.CharField( required = True , max_length = MAX_USERNAME_LENGTH , min_length = MIN_USERNAME_LENGTH )
    password = forms.CharField( required = True , max_length = MAX_PASSWORD_LENGTH , min_length = MIN_PASSWORD_LENGTH )
    email = forms.EmailField( required = True )

    def clean( self ):
        from re import compile, search
        cleaned_data = super().clean()
        username = cleaned_data.get( 'username' )
        password = cleaned_data.get( 'password' )
        email = cleaned_data.get( 'email' )
        if username and get_object_or_None( User , username = username ) is not None:
            self.add_error( 'username' , 'Username already exists.' )
        if password and compile( '[a-zA-Z]' ).search( password ) is None:
            self.add_error( 'password' , 'Password should contain at least one lowercase or uppercase letter.' )
        if email and get_object_or_None( User , email = email ) is not None:
            self.add_error( 'email' , 'Email already exists.' )
        return cleaned_data