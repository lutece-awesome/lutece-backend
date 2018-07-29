from django.db import models, transaction
from user.models import User
from discussion.models import Discussion
import django.utils.timezone as timezone
from discussion.models import Discussion
from uuslug import uuslug
# Create your models here.

class Blog( models.Model ):
    content = models.TextField( default = '' )
    title = models.CharField( max_length = 128 , default = '' )
    user = models.OneToOneField( User , null = True ,  on_delete = models.SET_NULL )
    create_time = models.DateTimeField ( default = timezone.now )
    slug = models.CharField( blank = True , max_length = 256 )
    view = models.IntegerField( default = 0 )

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = uuslug( self.title, instance = self )
        super( Blog , self ).save( * args , ** kwargs )

class BlogVoteUser( models.Model ):
    user = models.OneToOneField( User , null = True , on_delete = models.SET_NULL )
    blog = models.OneToOneField( Blog , null = True , on_delete = models.SET_NULL )
    vote = models.IntegerField( default = 0 )

class BlogDiscussion( Discussion ):
    blog = models.ForeignKey( Blog  , null = True , on_delete = models.SET_NULL)