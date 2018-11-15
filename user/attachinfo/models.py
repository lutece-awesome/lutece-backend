from django.db import models

from user.attachinfo.constant import MAX_SCHOOL_LENGTH, MAX_COMPANY_LENGTH, MAX_LOCATION_LENGTH, MAX_ABOUT_LENGTH, \
    DEFAULT_ABOUT, MAX_GRAVATAR_LENGTH


class AttachInfo(models.Model):
    school = models.CharField(max_length=MAX_SCHOOL_LENGTH, blank=True)
    company = models.CharField(max_length=MAX_COMPANY_LENGTH, blank=True)
    location = models.CharField(max_length=MAX_LOCATION_LENGTH, blank=True)
    about = models.CharField(max_length=MAX_ABOUT_LENGTH, blank=True, default=DEFAULT_ABOUT)
    gravatar = models.CharField(max_length=MAX_GRAVATAR_LENGTH, blank=True)
