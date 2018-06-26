from django.db import models
from user.models import User
from discussion.models import Discussion
# Create your models here.


class Blog( models.Model ):
    content = models.TextField( default = '' )
    title = models.CharField( max_length = 128 , default = '' )
    user = models.OneToOneField( User, on_delete = models.SET_NULL )
    discussion = models.ForeignKey(Discussion, on_delete=models.SET_NULL)
    create_time = models.DateTimeField(
        'Submit time', null=True, default=timezone.now)