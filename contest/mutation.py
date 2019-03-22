import graphene
import json
from annoying.functions import get_object_or_None
from django.conf import settings
from django.utils import timezone
from django.utils.datetime_safe import datetime
from graphql import ResolveInfo, GraphQLError
from graphql_jwt.decorators import permission_required, login_required

from contest.decorators import check_contest_permission
from contest.form import ContestForm, CreateContestClarificationForm, ContestSubmissionForm, CreateContestTeamForm, \
    ExitContestTeamForm, ToggleContestTeamForm, JoinContestTeamForm, UpdateContestTeamForm, UpdateContestForm
from contest.models import Contest, ContestSettings, ContestProblem, ContestClarification, ContestTeamMember, \
    ContestSubmission, ContestTeam
from data.service import DataService
from judge.models import JudgeResult as JudgeResultModel
from judge.result import JudgeResult
from judge.tasks import apply_submission
from problem.models import Problem
from submission.models import SubmissionAttachInfo
from user.models import User
from utils.function import assign


class CreateContest(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        note = graphene.String(required=True)
        disable = graphene.Boolean(required=True)
        start_time = graphene.DateTime(required=True)
        end_time = graphene.DateTime(required=True)
        max_team_member_number = graphene.Int(required=True)
        is_public = graphene.Boolean(required=True)
        problems = graphene.String(required=True)

    pk = graphene.ID()

    @permission_required('contest.add_contest')
    def mutate(self, info: ResolveInfo, **kwargs):
        form = ContestForm(kwargs)
        if form.is_valid():
            values = form.cleaned_data
            values['start_time'] = timezone.localtime(values['start_time']).replace(tzinfo=None)
            values['end_time'] = timezone.localtime(values['end_time']).replace(tzinfo=None)
            problems = json.loads(values.get('problems'))
            contest = Contest()
            settings = ContestSettings()
            assign(settings, **values)
            settings.save()
            contest.title = values.get('title')
            contest.settings = settings
            contest.save()
            for each in problems:
                ContestProblem(
                    contest=contest,
                    problem=Problem.objects.get(pk=each)
                ).save()
            return CreateContest(pk=contest.pk)
        else:
            raise RuntimeError(form.errors.as_json())


class UpdateContest(graphene.Mutation):
    class Arguments:
        pk = graphene.ID(required=True)
        title = graphene.String(required=True)
        note = graphene.String(required=True)
        disable = graphene.Boolean(required=True)
        start_time = graphene.DateTime(required=True)
        end_time = graphene.DateTime(required=True)
        max_team_member_number = graphene.Int(required=True)
        is_public = graphene.Boolean(required=True)
        problems = graphene.String(required=True)

    pk = graphene.ID()

    @permission_required('contest.change_contest')
    def mutate(self, info: ResolveInfo, **kwargs):
        form = UpdateContestForm(kwargs)
        if form.is_valid():
            values = form.cleaned_data
            values['start_time'] = timezone.localtime(values['start_time']).replace(tzinfo=None)
            values['end_time'] = timezone.localtime(values['end_time']).replace(tzinfo=None)
            problems = json.loads(values.get('problems'))
            contest = Contest.objects.get(pk=values.get('pk'))
            contest.title = values.get('title')
            contest.settings.note = values.get('note')
            contest.settings.disable = values.get('disable')
            contest.settings.start_time = values.get('start_time')
            contest.settings.end_time = values.get('end_time')
            contest.settings.max_team_member_number = values.get('max_team_member_number')
            contest.settings.is_public = values.get('is_public')
            contest.settings.save()
            contest.save()
            ContestProblem.objects.filter(contest=contest).delete()
            for each in problems:
                ContestProblem(
                    contest=contest,
                    problem=Problem.objects.get(pk=each)
                ).save()
            return UpdateContest(pk=contest.pk)
        else:
            raise RuntimeError(form.errors.as_json())


class CreateContestClarification(graphene.Mutation):
    class Arguments:
        pk = graphene.ID(required=True)
        content = graphene.String(required=True)
        reply = graphene.ID(required=False)

    pk = graphene.ID()

    @check_contest_permission
    def mutate(self: None, info: ResolveInfo, **kwargs):
        form = CreateContestClarificationForm(kwargs)
        if form.is_valid():
            values = form.cleaned_data
            contest = Contest.objects.get(pk=values.get('pk'))
            reply = values.get('reply')
            privilege = info.context.user.has_perm('contest.view_contest')
            if datetime.now() < contest.settings.start_time and not privilege:
                raise GraphQLError('Time denied')
            if reply:
                reply = ContestClarification.objects.get(pk=reply)
            comment = ContestClarification.objects.create(
                contest=contest,
                content=values.get('content'),
                reply=reply,
                author=info.context.user
            )
            return CreateContestClarification(pk=comment.pk)
        else:
            raise GraphQLError(form.errors.as_json())


class ContestSubmitSubmission(graphene.Mutation):
    class Arguments:
        problem_slug = graphene.String(required=True)
        code = graphene.String(required=True)
        language = graphene.String(required=True)
        pk = graphene.ID(required=True)

    pk = graphene.ID()

    @check_contest_permission
    def mutate(self, info: ResolveInfo, *args, **kwargs):
        if not info.context.user.is_authenticated:
            raise GraphQLError('Permission Denied')
        form = ContestSubmissionForm(kwargs)
        if form.is_valid():
            values = form.cleaned_data
            contest = Contest.objects.get(pk=values.get('pk'))
            privilege = info.context.user.has_perm('contest.view_contest')
            current_time = datetime.now()
            if (current_time < contest.settings.start_time or current_time > contest.settings.end_time) \
                    and not privilege:
                raise GraphQLError('Time denied')
            problem = get_object_or_None(Problem, slug=values['problem_slug'])
            attach_info = SubmissionAttachInfo(cases_count=DataService.get_cases_count(problem.pk))
            result = JudgeResultModel(_result=JudgeResult.PD.full)
            team_member = get_object_or_None(ContestTeamMember, user=info.context.user, contest_team__contest=contest,
                                             confirmed=True)
            if (not team_member or not team_member.confirmed or not team_member.contest_team.approved) \
                    and not info.context.user.has_perm('contest.view_contest'):
                raise GraphQLError('Permission Denied')
            sub = ContestSubmission(
                code=values.get('code'),
                _language=values.get('language'),
                user=info.context.user,
                problem=problem,
                contest=contest,
                team=team_member.contest_team if team_member else None,
                submission_type=1
            )
            attach_info.save()
            result.save()
            sub.attach_info = attach_info
            sub.result = result
            sub.save()
            apply_submission.apply_async(args=(sub.get_judge_field(),), queue=settings.JUDGE.get('task_queue'))
            problem.ins_submit_times()
            return ContestSubmitSubmission(pk=sub.pk)
        else:
            raise RuntimeError(form.errors.as_json())


class CreateContestTeam(graphene.Mutation):
    class Arguments:
        pk = graphene.ID(required=True)
        members = graphene.String(required=True)
        name = graphene.String(required=True)
        additional_info = graphene.String(required=False)

    state = graphene.Boolean()

    @login_required
    def mutate(self, info: ResolveInfo, *args, **kwargs):
        form = CreateContestTeamForm(kwargs)
        if form.is_valid():
            values = form.cleaned_data
            contest = Contest.objects.get(pk=values.get('pk'))
            current_time = datetime.now()
            usr = info.context.user
            if current_time > contest.settings.end_time:
                raise GraphQLError('Time denied')
            if get_object_or_None(ContestTeam, contest=contest, owner=usr):
                raise GraphQLError('Only one team can be created in one contest')
            if get_object_or_None(ContestTeamMember, contest_team__contest=contest, user=usr, confirmed=True):
                raise GraphQLError('To create a team, must exit the previous one')
            members = json.loads(values.get('members'))
            usr = info.context.user
            if usr.username not in members:
                raise GraphQLError('No owner')
            team = ContestTeam.objects.create(
                contest=contest,
                name=values.get('name'),
                owner=info.context.user,
                additional_info=values.get('additional_info')
            )
            for each in members:
                ContestTeamMember.objects.create(
                    contest_team=team,
                    user=User.objects.get(username=each),
                    confirmed=True if each == usr.username else False
                )
            return CreateContestTeam(state=True)
        else:
            raise RuntimeError(form.errors.as_json())


# If team member call this function, would exit team, if owner or user with delete permission, delete the entire team.
class ExitContestTeam(graphene.Mutation):
    class Arguments:
        pk = graphene.ID()

    state = graphene.Boolean()

    @login_required
    def mutate(self, info: ResolveInfo, *args, **kwargs):
        form = ExitContestTeamForm(kwargs)
        if form.is_valid():
            values = form.cleaned_data
            team = ContestTeam.objects.get(pk=values.get('pk'))
            contest = team.contest
            current_time = datetime.now()
            if current_time > contest.settings.end_time:
                raise GraphQLError('Time denied')
            usr = info.context.user
            # If owner exit, delete the entire team
            if team.owner == usr:
                team.memeber.all().delete()
                team.delete()
            else:
                member = team.memeber.get(user=usr)
                member.confirmed = False
                member.save()
                team.approved = False
                team.save()
            return ExitContestTeam(state=True)
        else:
            raise RuntimeError(form.errors.as_json())


class ToggleContestTeam(graphene.Mutation):
    class Arguments:
        pk = graphene.ID()

    state = graphene.Boolean()

    @permission_required('contest.change_contestteam')
    def mutate(self, info: ResolveInfo, *args, **kwargs):
        form = ToggleContestTeamForm(kwargs)
        if form.is_valid():
            values = form.cleaned_data
            team = ContestTeam.objects.get(pk=values.get('pk'))
            team.approved = False if team.approved else True
            team.save()
            return ToggleContestTeam(state=team.approved)
        else:
            raise RuntimeError(form.errors.as_json())


class JoinContestTeam(graphene.Mutation):
    class Arguments:
        pk = graphene.ID()

    state = graphene.Boolean()

    @login_required
    def mutate(self, info: ResolveInfo, *args, **kwargs):
        form = JoinContestTeamForm(kwargs)
        if form.is_valid():
            values = form.cleaned_data
            usr = info.context.user
            team = ContestTeam.objects.get(pk=values.get('pk'))
            if get_object_or_None(ContestTeamMember, contest_team__contest=team.contest, user=usr, confirmed=True):
                raise GraphQLError('To join other team, must exit the previous one.')
            member = team.memeber.get(user=usr)
            member.confirmed = True
            member.save()
            return JoinContestTeam(state=True)
        else:
            raise RuntimeError(form.errors.as_json())


class UpdateContestTeam(graphene.Mutation):
    class Arguments:
        pk = graphene.ID(required=True)
        members = graphene.String(required=True)
        name = graphene.String(required=True)
        additional_info = graphene.String(required=False)

    state = graphene.Boolean()

    @login_required
    def mutate(self, info: ResolveInfo, *args, **kwargs):
        form = UpdateContestTeamForm(kwargs)
        if form.is_valid():
            values = form.cleaned_data
            team = ContestTeam.objects.get(pk=values.get('pk'))
            current_time = datetime.now()
            if current_time > team.contest.settings.end_time:
                raise GraphQLError('Time denied')
            members = json.loads(values.get('members'))
            usr = info.context.user
            contain_owner = usr.username in members
            if (not contain_owner or team.owner != usr) and not usr.has_perm('contest.change_contestteam'):
                raise GraphQLError('No owner or permission denied')
            name = values.get('name')
            additional_info = values.get('additional_info')
            if name != team.name or additional_info != team.additional_info or set(
                    map(lambda each: each.user.username, team.memeber.all())) != set(members):
                team.approved = False
            team.name = name
            team.additional_info = additional_info
            team.save()
            for each in team.memeber.all():
                if each.user.username not in members:
                    each.delete()
            for each in members:
                ContestTeamMember.objects.get_or_create(
                    contest_team=team,
                    user=User.objects.get(username=each)
                )
            return UpdateContestTeam(state=True)
        else:
            raise RuntimeError(form.errors.as_json())


class Mutation(graphene.AbstractType):
    create_contest = CreateContest.Field()
    update_contest = UpdateContest.Field()
    create_contest_clarification = CreateContestClarification.Field()
    contest_submit_submission = ContestSubmitSubmission.Field()
    create_contest_team = CreateContestTeam.Field()
    exit_contest_team = ExitContestTeam.Field()
    toggle_contest_team = ToggleContestTeam.Field()
    join_contest_team = JoinContestTeam.Field()
    update_contest_team = UpdateContestTeam.Field()
