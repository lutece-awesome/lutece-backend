from django.db import models
from django.utils import timezone

from reply.constant import MAX_CONTENT_LENGTH
from user.models import User


class BaseReply(models.Model):
    content = models.CharField(max_length=MAX_CONTENT_LENGTH, blank=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    reply = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, db_index=True, related_name='reply_node')
    ancestor = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, db_index=True,
                                 related_name='ancestor_node')
    create_time = models.DateField(default=timezone.now)
    disable = models.BooleanField(default=False, db_index=True)
    create_time = models.DateTimeField(default=timezone.now)
    last_update_time = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        self.last_update_time = timezone.now()
        super().save(*args, **kwargs)
