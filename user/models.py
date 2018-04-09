from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class user(AbstractUser):
    last_name = None
    first_name = None
    displayName = models.CharField( max_length = 128 )