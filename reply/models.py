from django.db import models
from django.utils import timezone
from reply.constant import MAX_CONTENT_LENGTH, MAX_ATTITUDE_LENGTH
from user.models import User
from record.models import DetailedRecord
from enum import Enum

class AbstractReply( models.Model ):
    content = models.CharField( max_length = MAX_CONTENT_LENGTH , blank = True )
    parent = models.ForeignKey( 'self' , on_delete = models.SET_NULL , null = True , db_index = True , related_name = 'parent' )
    ancestor = models.ForeignKey( 'self' , on_delete = models.SET_NULL , null = True , db_index = True , related_name = 'ancestor' )
    create_time = models.DateField( default = timezone.now )
    user = models.ForeignKey( User , on_delete = models.SET_NULL , null = True )
    disable = models.BooleanField( default = False , db_index = True )

class Attitude:
    agree = 'Agree'
    neutral = 'Neutral'
    disagree = 'Disagree'
    choice = {
        ( agree , 'Agree this discussion' ),
        ( neutral , 'Only god knows its attitude' ),
        ( disagree , 'Disagree this discussion' ),
    }

class AbstractReplyVote( DetailedRecord ):
    reply = models.ForeignKey( AbstractReply , on_delete = models.SET_NULL , null = True )
    attitude = models.CharField( choices = Attitude.choice , default = Attitude.neutral , max_length = MAX_ATTITUDE_LENGTH , db_index = True )