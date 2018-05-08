from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Userinfo


class Inline_info(admin.StackedInline):
    model = Userinfo 


class UserAdmin(admin.ModelAdmin):
    inlines = (Inline_info ,)

admin.site.register( User , UserAdmin )
