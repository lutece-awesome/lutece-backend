from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core import serializers
from django.contrib.auth.hashers import make_password
# Create your models here.


class user(AbstractUser):
    last_name = None
    first_name = None
    displayName = models.CharField( max_length = 128 )

    def __str__(self):
        return self.username
