from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import Discussion

admin.site.register(Discussion, MPTTModelAdmin)