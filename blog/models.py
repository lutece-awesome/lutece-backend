from django.db import models
from user.models import User
from discussion.models import Discussion
import django.utils.timezone as timezone
# Create your models here.


class Blog( models.Model ):
    content = models.TextField( default = '' )
    title = models.CharField( max_length = 128 , default = '' )
    user = models.OneToOneField( User , null = True ,  on_delete = models.SET_NULL )
    discussion = models.ForeignKey(Discussion , null = True , on_delete = models.SET_NULL)
    create_time = models.DateTimeField ( default=timezone.now )

class BlogVoteUser( models.Model ):
    user = models.OneToOneField( User , null = True , on_delete = models.SET_NULL )
    blog = models.OneToOneField( Blog , null = True , on_delete = models.SET_NULL )
    vote = models.IntegerField( default = 0 )