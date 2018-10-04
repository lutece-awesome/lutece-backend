from django.db import models
from django.contrib.auth.models import AbstractUser
from user.attachinfo.models import AttachInfo

class User( AbstractUser ):
    attach_info = models.OneToOneField( AttachInfo , on_delete = models.CASCADE )
    solved = models.IntegerField( default = 0 )
    tried = models.IntegerField( default = 0 )
    
    def __str__(self):
        return self.username