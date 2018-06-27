from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from user.models import User
import django.utils.timezone as timezone


class Discussion(MPTTModel):
    discussion_id = models.AutoField(primary_key=True)
    content = models.CharField(max_length=200, blank=True, null=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE,
                            null=True, blank=True, related_name='children')
    submit_time = models.DateTimeField(
        'Submit time', null=True, default=timezone.now)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    visibility = models.BooleanField(default=True)

    @classmethod
    def get_new(cls):
        return cls.objects.create().discussion_id
    
    class Meta:
        ordering = ['-discussion_id']
        permissions = (
            ('view_all' , 'Can view all discussion'),
            ('change_visibility' , 'Can toggle discussion visibility status' ),
        )