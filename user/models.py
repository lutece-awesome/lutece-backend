from django.db import models
from django.contrib.auth.models import AbstractUser
from user.attachinfo import AttachInfo
from user.constant import MAX_GRAVATAR_LENGTH

class User( AbstractUser ):
    attach_info = models.OneToOneField( AttachInfo , on_delete = models.CASCADE )
    
    def __str__(self):
        return self.username