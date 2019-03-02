import json
from django import forms
from django.utils import timezone

from contest.constant import MAX_CONTEST_TITLE_LENGTH, MAX_CONTEST_TEAM_MEMBER, MIN_CONTEST_TEAM_MEMBER, \
    MAX_CONTEST_PASSWORD_LENGTH
from problem.models import Problem


class ContestSettingForm(forms.Form):
    title = forms.CharField(required=True, min_length=1, max_length=MAX_CONTEST_TITLE_LENGTH)
    note = forms.CharField(required=False)
    disable = forms.BooleanField(required=False)
    start_time = forms.DateTimeField(required=False)
    end_time = forms.DateTimeField(required=False)
    max_team_member_number = forms.IntegerField(required=False, min_value=MIN_CONTEST_TEAM_MEMBER,
                                                max_value=MAX_CONTEST_TEAM_MEMBER)
    password = forms.CharField(required=False, max_length=MAX_CONTEST_PASSWORD_LENGTH)
    can_join_after_contest_begin = forms.BooleanField(required=False)
    join_need_approve = forms.BooleanField(required=False)

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        if start_time >= end_time:
            self.add_error('start_time', 'Start time could not before the end time')
        elif start_time.replace(tzinfo=None) <= timezone.now():
            self.add_error('start_time', 'Start time could not before the current time')
        return cleaned_data


class ContestProblemForm(forms.Form):
    problems = forms.CharField(required=True)

    def clean(self):
        cleaned_data = super().clean()
        problems = cleaned_data.get('problems')
        problem_pk_arr = json.loads(problems)
        problem_arr = list()
        for each_pk in problem_pk_arr:
            problem_arr.append(Problem.objects.get(pk=each_pk))
        if len(problem_arr) != len(problem_pk_arr):
            self.add_error('problems', 'No duplicated problem allowded')
        return cleaned_data


class ContestForm(ContestProblemForm, ContestSettingForm):

    def clean(self):
        return super().clean()
