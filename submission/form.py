from annoying.functions import get_object_or_None
from django import forms

from judge.language import Language
from problem.models import Problem
from submission.constant import MAX_CODE_LENGTH


class SubmitSubmissionForm(forms.Form):
    problem_slug = forms.CharField(required=True)
    code = forms.CharField(required=True, max_length=MAX_CODE_LENGTH, min_length=1)
    language = forms.CharField(required=True)

    def clean(self):
        cleaned_data = super().clean()
        problemslug = cleaned_data.get('problem_slug')
        code = cleaned_data.get('code')
        language = Language.value_of(cleaned_data.get('language'))
        prob = get_object_or_None(Problem, slug=problemslug)
        if problemslug and not prob:
            self.add_error('problemslug', 'Problem not exists.')
        if not language:
            self.add_error('language', 'Unknown language')
        return cleaned_data
