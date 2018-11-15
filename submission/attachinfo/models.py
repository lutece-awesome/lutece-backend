from django.db import models


class AbstractAttachInfo(models.Model):
    class Meta:
        abstract = True

    visibility = models.BooleanField(default=False)
