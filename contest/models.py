import django.utils.timezone as timezone
from django.db import models

from contest.constant import MAX_CONTEST_TITLE_LENGTH, MAX_CONTEST_PASSWORD_LENGTH, MAX_CONTEST_TEAM_NAME_LENGTH
from problem.models import Problem
from reply.models import BaseReply
from submission.models import Submission
from user.models import User


class ContestSettings(models.Model):
    note = models.TextField(blank=True)
    disable = models.BooleanField(default=False)
    start_time = models.DateTimeField(null=False, default=timezone.now)
    end_time = models.DateTimeField(null=False, default=timezone.now)
    max_team_member_number = models.IntegerField(default=1)
    password = models.CharField(max_length=MAX_CONTEST_PASSWORD_LENGTH)
    can_join_after_contest_begin = models.BooleanField(default=False)
    join_need_approve = models.BooleanField(default=False)


class Contest(models.Model):
    title = models.CharField(max_length=MAX_CONTEST_TITLE_LENGTH, blank=True, unique=True)
    settings = models.OneToOneField(ContestSettings, on_delete=models.CASCADE)

    def is_public(self):
        return len(self.settings.password) == 0


class ContestProblem(models.Model):
    contest = models.ForeignKey(Contest, on_delete=models.SET_NULL, null=True)
    problem = models.ForeignKey(Problem, on_delete=models.SET_NULL, null=True)


class ContestTeam(models.Model):
    contest = models.ForeignKey(Contest, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=MAX_CONTEST_TEAM_NAME_LENGTH, unique=True)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    approved = models.BooleanField(default=False)

    def member_list(self):
        return self.memeber.all()


class ContestTeamMember(models.Model):
    contest_team = models.ForeignKey(ContestTeam, on_delete=models.SET_NULL, null=True, related_name='memeber')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    confirmed = models.BooleanField(default=True)


# SubmissionType = 1
class ContestSubmission(Submission):
    contest = models.ForeignKey(Contest, on_delete=models.SET_NULL, null=True)
    team = models.ForeignKey(ContestTeam, on_delete=models.SET_NULL, null=True)


class ContestClarification(BaseReply):
    contest = models.ForeignKey(Contest, on_delete=models.SET_NULL, null=True)
