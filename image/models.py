from django.db import models
import django.utils.timezone as timezone
from user.models import User
from image.constant import UPLOAD_IMAGE_PATH
# Create your models here.

class Image( models.Model ):
    user = models.ForeignKey( User, on_delete = models.SET_NULL , null = True , db_index = True )
    upload_time = models.DateTimeField( default = timezone.now )
    image = models.ImageField( upload_to = UPLOAD_IMAGE_PATH )