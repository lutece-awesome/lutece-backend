from django import forms
from image.constant import MAX_IMAGE_SIZE

class UploadImageForm( forms.Form ):
    image = forms.ImageField( required = True )

    def clean( self ):
        cleaned_data = super().clean()
        image = cleaned_data.get( 'image' )
        if image and image.size > MAX_IMAGE_SIZE:
            self.add_error( 'image' , 'Image size can not exceed 2mb' )