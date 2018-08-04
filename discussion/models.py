from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from user.models import User
import django.utils.timezone as timezone

class Discussion(models.Model):
    discussion_id = models.AutoField(primary_key=True)
    content = models.CharField(max_length=200, blank=True, null=True)
    reply = models.ForeignKey( 'self' , on_delete = models.SET_NULL , null = True , blank = True , db_index = True , related_name = 'discussion_reply' )
    ancestor = models.ForeignKey( 'self' , on_delete = models.SET_NULL , null = True , blank = True , db_index = True , related_name = 'discussion_ancestor' )
    submit_time = models.DateTimeField(
        'Submit time', null=True, default=timezone.now)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    visibility = models.BooleanField( default=True , db_index = True )
    vote = models.IntegerField( default = 0 )

    @classmethod
    def get_new(cls):
        return cls.objects.create().discussion_id
    
    class Meta:
        permissions = (
            ('view_all' , 'Can view all discussion'),
            ('change_visibility' , 'Can toggle discussion visibility status' ),
        )

class DiscussionVote( models.Model ):
    discussion = models.ForeignKey( Discussion , null = True , on_delete = models.SET_NULL )
    user = models.ForeignKey( User , null = True , on_delete = models.SET_NULL )
    vote = models.BooleanField( default = True )