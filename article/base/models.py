import django.utils.timezone as timezone
from django.db import models

from article.base.constant import MAX_TITLE_LENGTH
from user.models import User


class AbstractArticle(models.Model):
    class Meta:
        abstract = True

    title = models.CharField(max_length=MAX_TITLE_LENGTH, blank=True)
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    create_time = models.DateTimeField(default=timezone.now)
    last_update_time = models.DateTimeField(default=timezone.now)
    disable = models.BooleanField(default=False)
    content = models.TextField(blank=True)

    def __str__(self):
        return f'Article<{self.title}>'

    def save(self, *args, **kwargs):
        self.last_update_time = timezone.now()
        super().save(*args, **kwargs)
