from django.db import models, transaction
from user.models import User
from discussion.models import Discussion
import django.utils.timezone as timezone
from discussion.models import Discussion
# Create your models here.

class BlogDiscussion( Discussion ):
    pass

class Blog( models.Model ):
    content = models.TextField( default = '' )
    title = models.CharField( max_length = 128 , default = '' )
    user = models.OneToOneField( User , null = True ,  on_delete = models.SET_NULL )
    discussion = models.ForeignKey(BlogDiscussion , null = True , on_delete = models.SET_NULL)
    create_time = models.DateTimeField ( default = timezone.now )

class BlogVoteUser( models.Model ):
    user = models.OneToOneField( User , null = True , on_delete = models.SET_NULL )
    blog = models.OneToOneField( Blog , null = True , on_delete = models.SET_NULL )
    vote = models.IntegerField( default = 0 )