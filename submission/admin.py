from django.contrib import admin
from .models import Submission, Judgeinfo


class Inline(admin.StackedInline):
    model = Judgeinfo


class SubmissionAdmin(admin.ModelAdmin):
    inlines = (Inline,)


admin.site.register( Submission , SubmissionAdmin)
admin.site.register( Judgeinfo )