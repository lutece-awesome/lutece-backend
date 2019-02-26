import django.utils.timezone as timezone
from django.db import models

from contest.constant import MAX_TEAM_NAME_LENGTH, MAX_CONTEST_TITLE_LENGTH
from problem.models import Problem
from user.models import User


class ContestSettings(models.Model):
    note = models.TextField(blank=True)
    disable = models.BooleanField(default=False)
    start_time = models.DateTimeField(null=False, default=timezone.now)
    end_time = models.DateTimeField(null=False, default=timezone.now)
    max_team_member_number = models.IntegerField(default=1)


class Contest(models.Model):
    title = models.CharField(max_length=MAX_CONTEST_TITLE_LENGTH, blank=True, unique=True)
    settings = models.OneToOneField(ContestSettings, on_delete=models.CASCADE)


class ContestProblem(models.Model):
    contest = models.ForeignKey(Contest, on_delete=models.SET_NULL, null=True)
    problem = models.ForeignKey(Problem, on_delete=models.SET_NULL, null=True)


class ContestTeam(models.Model):
    contest = models.ForeignKey(Contest, on_delete=models.SET_NULL, null=True)
    team_name = models.CharField(max_length=MAX_TEAM_NAME_LENGTH)


class ContestTeamMember(models.Model):
    contest_team = models.ForeignKey(ContestTeam, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
