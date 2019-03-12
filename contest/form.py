import json
from annoying.functions import get_object_or_None
from django import forms
from django.utils import timezone

from contest.constant import MAX_CONTEST_TITLE_LENGTH, MAX_CONTEST_TEAM_MEMBER, MIN_CONTEST_TEAM_MEMBER, \
    MAX_CONTEST_PASSWORD_LENGTH, MAX_USER_LIST_LENGTH, MAX_CONTEST_TEAM_NAME_LENGTH
from contest.models import Contest, ContestClarification, ContestTeam
from problem.models import Problem
from reply.constant import MAX_CONTENT_LENGTH
from submission.form import SubmitSubmissionForm
from user.models import User


class ContestSettingForm(forms.Form):
    title = forms.CharField(required=True, min_length=1, max_length=MAX_CONTEST_TITLE_LENGTH)
    note = forms.CharField(required=False)
    disable = forms.BooleanField(required=False)
    start_time = forms.DateTimeField(required=False)
    end_time = forms.DateTimeField(required=False)
    max_team_member_number = forms.IntegerField(required=False, min_value=MIN_CONTEST_TEAM_MEMBER,
                                                max_value=MAX_CONTEST_TEAM_MEMBER)
    password = forms.CharField(required=False, max_length=MAX_CONTEST_PASSWORD_LENGTH)

    def clean(self):
        cleaned_data = super().clean()
        start_time = timezone.localtime(cleaned_data.get('start_time')).replace(tzinfo=None)
        end_time = timezone.localtime(cleaned_data.get('end_time')).replace(tzinfo=None)
        if start_time >= end_time:
            self.add_error('start_time', 'Start time could not before the end time')
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
        elif len(problem_arr) > 26:
            self.add_error('problem', 'At most 26 problems')
        return cleaned_data


class ContestForm(ContestProblemForm, ContestSettingForm):

    def clean(self):
        return super().clean()


class UpdateContestForm(ContestForm):
    pk = forms.IntegerField(required=True)


class CreateContestClarificationForm(forms.Form):
    pk = forms.IntegerField(required=True)
    content = forms.CharField(max_length=MAX_CONTENT_LENGTH)
    reply = forms.IntegerField(required=False)

    def clean(self) -> dict:
        cleaned_data = super().clean()
        pk = cleaned_data.get('pk')
        if pk and not get_object_or_None(Contest, pk=pk):
            self.add_error("pk", "No such contest")
        reply = cleaned_data.get('reply')
        if reply and not get_object_or_None(ContestClarification, pk=reply):
            self.add_error("reply", "No such reply node")
        return cleaned_data


# Check time on main logic
class ContestSubmissionForm(SubmitSubmissionForm):
    pk = forms.IntegerField(required=True)

    def clean(self) -> dict:
        cleaned_data = super().clean()
        pk = cleaned_data.get('pk')
        contest = get_object_or_None(Contest, pk=pk)
        if pk and not contest:
            self.add_error("pk", "No such contest")
        return cleaned_data


class CreateContestTeamForm(forms.Form):
    pk = forms.IntegerField(required=True)
    members = forms.CharField(max_length=MAX_USER_LIST_LENGTH)
    name = forms.CharField(max_length=MAX_CONTEST_TEAM_NAME_LENGTH)

    def clean(self) -> dict:
        cleaned_data = super().clean()
        pk = cleaned_data.get('pk')
        name = cleaned_data.get('name')
        contest = get_object_or_None(Contest, pk=pk)
        if pk and not contest:
            self.add_error("pk", "No such contest")
        members = json.loads(cleaned_data.get('members'))
        if len(members) + 1 > contest.settings.max_team_member_number:
            self.add_error('members', 'Team Size exceeded')
        if len(set(members)) != len(members):
            self.add_error('members', 'Duplicate users')
        else:
            for each in members:
                usr = get_object_or_None(User, username=each)
                if not usr:
                    self.add_error('members', 'no such user')
        if get_object_or_None(ContestTeam, contest=contest, name=name):
            self.add_error('name', 'duplicate team name')
        return cleaned_data


class ExitContestTeamForm(forms.Form):
    pk = forms.IntegerField(required=True)

    def clean(self) -> dict:
        cleaned_data = super().clean()
        pk = cleaned_data.get('pk')
        contest_team = get_object_or_None(ContestTeam, pk=pk)
        if not contest_team:
            self.add_error("team_pk", "No such team")
        return cleaned_data


class ToggleContestTeamForm(forms.Form):
    pk = forms.IntegerField(required=True)

    def clean(self) -> dict:
        cleaned_data = super().clean()
        pk = cleaned_data.get('pk')
        contest_team = get_object_or_None(ContestTeam, pk=pk)
        if not contest_team:
            self.add_error("pk", "No such team")
        return cleaned_data


class JoinContestTeamForm(forms.Form):
    pk = forms.IntegerField(required=True)

    def clean(self) -> dict:
        cleaned_data = super().clean()
        pk = cleaned_data.get('pk')
        team = get_object_or_None(ContestTeam, pk=pk)
        if not team:
            self.add_error('pk', 'no such team')
        return cleaned_data


class UpdateContestTeamForm(forms.Form):
    pk = forms.IntegerField(required=True)
    members = forms.CharField(max_length=MAX_USER_LIST_LENGTH)
    name = forms.CharField(max_length=MAX_CONTEST_TEAM_NAME_LENGTH)

    def clean(self) -> dict:
        cleaned_data = super().clean()
        pk = cleaned_data.get('pk')
        name = cleaned_data.get('name')
        team = ContestTeam.objects.get(pk=pk)
        members = json.loads(cleaned_data.get('members'))
        if len(members) + 1 > team.contest.settings.max_team_member_number:
            self.add_error('members', 'Team Size exceeded')
        if len(set(members)) != len(members):
            self.add_error('members', 'Duplicate users')
        else:
            for each in members:
                usr = get_object_or_None(User, username=each)
                if not usr:
                    self.add_error('members', 'no such user')
        check_team = get_object_or_None(ContestTeam, contest=team.contest, name=name)
        if check_team and check_team != team:
            self.add_error('name', 'duplicate team name')
        return cleaned_data
