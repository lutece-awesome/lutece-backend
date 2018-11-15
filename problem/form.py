from annoying.functions import get_object_or_None
from django import forms

from problem.baseproblem.form import AbstractProblemForm
from problem.limitation.form import LimitationForm
from problem.models import Problem
from problem.sample.form import SampleForm


class UpdateProblemForm(AbstractProblemForm, LimitationForm, SampleForm):
    slug = forms.CharField(required=True)

    def clean(self, *args, **kwargs):
        cleaned_data = super().clean()
        slug = cleaned_data.get('slug')
        if not get_object_or_None(Problem, slug=slug):
            self.add_error('slug', 'Unknown problem for such slug.')
        return cleaned_data


class CreateProblemForm(AbstractProblemForm, LimitationForm, SampleForm):
    pass
