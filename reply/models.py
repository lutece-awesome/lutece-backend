from django.db import models
from django.utils import timezone

from reply.constant import MAX_CONTENT_LENGTH
from user.models import User


class BaseReply(models.Model):
    content = models.CharField(max_length=MAX_CONTENT_LENGTH, blank=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    reply = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, db_index=True, related_name='reply')
    create_time = models.DateField(default=timezone.now)
    disable = models.BooleanField(default=False, db_index=True)
