from django.db import models
import django.utils.timezone as timezone
from user.models import User

class UploadFile( models.Model ):
    user = models.ForeignKey( User, on_delete = models.CASCADE, null = True , blank = True , db_index = True )
    submit_time = models.DateTimeField( 'Submit time' , default = timezone.now )
    image = models.ImageField( upload_to = 'photo/%Y/%m/%d' )