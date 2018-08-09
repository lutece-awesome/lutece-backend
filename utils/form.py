from django import forms

class UploadImageForm( forms.Form ):
    image = forms.ImageField( required = True )


    def clean( self ):
        cleaned_data = super().clean()
        image = cleaned_data.get( 'image' )
        if image and image.size > 2 * 1024 * 1024:
            self.add_error( 'image' , 'Image size can not exceed 2mb' )