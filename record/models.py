import django.utils.timezone as timezone
from django.db import models

from user.models import User


# Create your models here.


class AbstractRecord(models.Model):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class DetailedRecord(AbstractRecord):
    record_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    record_time = models.DateTimeField(default=timezone.now, db_index=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class SimpleRecord(AbstractRecord):
    count = models.IntegerField(default=0)

    def __ins(self, add):
        self.count += add

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def increase(self):
        self.__ins(1)


class Attitude:
    agree = 'Agree'
    neutral = 'Neutral'
    disagree = 'Disagree'
    choice = {
        (agree, 'Agree this discussion'),
        (neutral, 'Only god knows its attitude'),
        (disagree, 'Disagree this discussion'),
    }

# class BaseReplyVote(DetailedRecord):
#     reply = models.ForeignKey(AbstractReply, on_delete=models.SET_NULL, null=True)
#     attitude = models.CharField(choices=Attitude.choice, default=Attitude.neutral, max_length=MAX_ATTITUDE_LENGTH,
#                                 db_index=True)
