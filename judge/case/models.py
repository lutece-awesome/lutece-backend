from django.db import models

class AbstractCase( models.Model ):

    class Meta:
        abstract = True

    time_cost = models.IntegerField( default = 0 )
    memory_cost = models.IntegerField( default = 0 )