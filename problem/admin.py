from django.contrib import admin
from .models import Problem, Sample, ProblemDiscussion
from django import forms

class SampleModelForm( forms.ModelForm ):
    input_content = forms.CharField( widget=forms.Textarea )
    output_content = forms.CharField( widget=forms.Textarea )
    class Meta:
        model = Sample
        fields = '__all__'

class SampleInline(admin.StackedInline):
    form = SampleModelForm
    model = Sample

class ProblemDiscussionInline(admin.StackedInline):
    model = ProblemDiscussion

class ProblemAdmin(admin.ModelAdmin):
    inlines = (SampleInline, ProblemDiscussionInline, )

admin.site.register(Problem, ProblemAdmin)
