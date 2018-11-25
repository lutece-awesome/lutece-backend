import django.utils.timezone as timezone
from django.db import models
from uuslug import uuslug

from user.models import User


class AbstractArticle(models.Model):
    class Meta:
        abstract = True

    title = models.CharField(max_length=128, blank=True)
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    create_time = models.DateTimeField(default=timezone.now)
    slug = models.CharField(blank=True, max_length=256)
    disable = models.BooleanField(default=False)
    content = models.TextField(blank=True)

    def __str__(self):
        return f'Article<{self.title}>'

    def save(self, *args, **kwargs):
        self.slug = uuslug(self.title, instance=True)
        super().save(*args, **kwargs)
