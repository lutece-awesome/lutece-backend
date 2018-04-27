from django.contrib import admin
from .models import Problem,Sample


class Inline(admin.StackedInline):
    model = Sample

class ProblemAdmin(admin.ModelAdmin):
    inlines = (Inline,)

admin.site.register(Problem , ProblemAdmin)
