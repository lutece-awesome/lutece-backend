from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Userinfo


class Inline(admin.StackedInline):
    model = Userinfo


class UserAdmin(admin.ModelAdmin):
    inlines = (Inline,)

admin.site.register( User , UserAdmin )
