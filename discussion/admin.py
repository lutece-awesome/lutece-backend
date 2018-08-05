from django.contrib import admin
from .models import Discussion, DiscussionVote

admin.site.register( Discussion , )
admin.site.register( DiscussionVote , )