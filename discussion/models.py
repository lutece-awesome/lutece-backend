from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

class Discussion(MPTTModel):
    content = models.CharField(max_length=200)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
