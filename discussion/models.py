from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from user.models import User
from record.models import DetailedRecord
import django.utils.timezone as timezone

class Discussion(models.Model):
    discussion_id = models.AutoField(primary_key=True)
    content = models.CharField(max_length = 1024, blank=True, null=True)
    reply = models.ForeignKey( 'self' , on_delete = models.SET_NULL , null = True , blank = True , db_index = True , related_name = 'discussion_reply' )
    ancestor = models.ForeignKey( 'self' , on_delete = models.SET_NULL , null = True , blank = True , db_index = True , related_name = 'discussion_ancestor' )
    submit_time = models.DateTimeField( null=True, default=timezone.now )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    visibility = models.BooleanField( default=True , db_index = True )
    vote = models.IntegerField( default = 0 )

    def refresh_vote( self ):
        self.vote = DiscussionVote.objects.filter( discussion = self , vote = DiscussionVote.agree ).count() - DiscussionVote.objects.filter( discussion = self , vote = DiscussionVote.disagree ).count()
        self.save()

    @classmethod
    def get_new(cls):
        return cls.objects.create().discussion_id
    
    class Meta:
        permissions = (
            ('view_all' , 'Can view all discussion'),
            ('change_visibility' , 'Can toggle discussion visibility status' ),
        )

class DiscussionVote( DetailedRecord ):
    discussion = models.ForeignKey( Discussion , null = True , on_delete = models.SET_NULL )
    agree = 'Agree'
    neutral = 'Neutral'
    disagree = 'Disagree'
    state_choice = {
        ( agree , 'Agree this discussion' ),
        ( neutral , 'Only god knows its attitude' ),
        ( disagree , 'Disagree this discussion' ),
    }
    vote = models.CharField( choices = state_choice , default = neutral , max_length = 12 , db_index = True )