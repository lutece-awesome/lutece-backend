from django.contrib import admin
from .models import Problem, Sample, ProblemDiscussion


class SampleInline(admin.StackedInline):
    model = Sample

class ProblemDiscussionInline(admin.StackedInline):
    model = ProblemDiscussion

class ProblemAdmin(admin.ModelAdmin):
    inlines = (SampleInline, ProblemDiscussionInline, )

admin.site.register(Problem, ProblemAdmin)
