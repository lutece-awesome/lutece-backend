import graphene
from annoying.functions import get_object_or_None
from django.db.models import Q
from django.utils.datetime_safe import datetime
from graphql import ResolveInfo
from graphql_jwt.decorators import permission_required

from contest.decorators import check_contest_permission
from contest.models import ContestTeamMember, ContestSubmission, Contest, ContestTeam, ContestProblem
from judge.result import JudgeResult
from problem.type import ProblemType
from reply.type import BaseReplyType
from user.type import UserType
from utils.interface import PaginatorList


class ContestProblemType(ProblemType):
    tried = graphene.Boolean()
    solved = graphene.Boolean()
    submit = graphene.Int()
    accept = graphene.Int()

    def resolve_tried(self, info: ResolveInfo) -> graphene.Boolean():
        usr = info.context.user
        if not usr.is_authenticated:
            return False
        contest = Contest.objects.get(pk=info.variable_values.get('pk'))
        team = get_object_or_None(ContestTeam, contest=contest, memeber__user=usr, memeber__confirmed=True)
        return ContestSubmission.objects.filter(contest=contest, team=team, problem=self).exists()

    def resolve_solved(self, info: ResolveInfo) -> graphene.Boolean():
        usr = info.context.user
        if not usr.is_authenticated:
            return False
        contest = Contest.objects.get(pk=info.variable_values.get('pk'))
        team = get_object_or_None(ContestTeam, contest=contest, memeber__user=usr, memeber__confirmed=True)
        return ContestSubmission.objects.filter(contest=contest, team=team, problem=self,
                                                result___result=JudgeResult.AC.full).exists()

    def resolve_submit(self, info: ResolveInfo) -> graphene.Int():
        contest = Contest.objects.get(pk=info.variable_values.get('pk'))
        return ContestSubmission.objects.filter(Q(contest=contest) & Q(problem=self) & ~Q(team=None)).count()

    def resolve_accept(self, info: ResolveInfo) -> graphene.Int():
        contest = Contest.objects.get(pk=info.variable_values.get('pk'))
        return ContestSubmission.objects.filter(
            Q(contest=contest) & Q(problem=self) & ~Q(team=None) & Q(result___result=JudgeResult.AC.full)).values(
            'team').distinct().count()


class ContestSettingsType(graphene.ObjectType):
    note = graphene.String()
    disable = graphene.Boolean()
    start_time = graphene.DateTime()
    end_time = graphene.DateTime()
    max_team_member_number = graphene.Int()
    password = graphene.String()

    def resolve_note(self, info: ResolveInfo) -> graphene.String():
        return self.note

    def resolve_disable(self, info: ResolveInfo) -> graphene.Boolean():
        return self.disable

    def resolve_start_time(self, info: ResolveInfo) -> graphene.DateTime():
        return self.start_time

    def resolve_end_time(self, info: ResolveInfo) -> graphene.DateTime():
        return self.end_time

    def resolve_max_team_member_number(self, info: ResolveInfo) -> graphene.Int():
        return self.max_team_member_number

    @permission_required('contest.view_contest')
    def resolve_password(self, info: ResolveInfo) -> graphene.String():
        return self.password


class ContestType(graphene.ObjectType):
    pk = graphene.ID()
    title = graphene.String()
    settings = graphene.Field(ContestSettingsType)
    registered = graphene.Boolean()
    register_member_number = graphene.Int()
    is_public = graphene.Boolean()
    problems = graphene.List(ContestProblemType)

    def resolve_pk(self, info: ResolveInfo) -> graphene.ID():
        return self.pk

    def resolve_title(self, info: ResolveInfo) -> graphene.String():
        return self.title

    def resolve_settings(self, info: ResolveInfo) -> ContestSettingsType:
        return self.settings

    def resolve_registered(self, info: ResolveInfo) -> graphene.Boolean():
        usr = info.context.user
        if not usr.is_authenticated:
            return False
        member = get_object_or_None(ContestTeamMember, user=usr, contest_team__contest=self, confirmed=True)
        return usr.has_perm('contest.view_contest') or (member and member.contest_team.approved)

    def resolve_register_member_number(self, info: ResolveInfo) -> graphene.Int():
        return ContestTeamMember.objects.filter(contest_team__contest=self, contest_team__approved=True,
                                                confirmed=True).count()

    def resolve_is_public(self, info: ResolveInfo) -> graphene.Boolean():
        return self.is_public()

    @check_contest_permission
    def resolve_problems(self, info: ResolveInfo):
        privilege = info.context.user.has_perm('contest.view_contestproblem')
        if datetime.now() < self.settings.start_time and not privilege:
            return []
        return map(lambda each: each.problem, ContestProblem.objects.filter(contest=self))


class ContestListType(graphene.ObjectType, interfaces=[PaginatorList]):
    contest_list = graphene.List(ContestType, )


# This is the duck type of Submission
class ContestRankingSubmissionType(graphene.ObjectType):
    status = graphene.String()
    create_time = graphene.DateTime()
    team = graphene.String()
    problem_id = graphene.String()

    def resolve_status(self, info: ResolveInfo) -> graphene.String():
        return self.judge_result

    def resolve_create_time(self, info: ResolveInfo) -> graphene.String():
        return self.create_time

    def resolve_team(self, info: ResolveInfo) -> graphene.String():
        return self.team_name

    def resolve_problem_id(self, info: ResolveInfo) -> graphene.String():
        return self.problem_id


class ContestClarificationType(BaseReplyType):
    pass


class ContestClarificationListType(graphene.ObjectType, interfaces=[PaginatorList]):
    contest_clarification_list = graphene.List(ContestClarificationType, )


class ContestTeamMemberType(graphene.ObjectType):
    user = graphene.Field(UserType)
    confirmed = graphene.Boolean()

    def resolve_user(self, info: ResolveInfo):
        return self.user

    def resolve_confirmed(self, info: ResolveInfo):
        return self.confirmed


class ContestTeamType(graphene.ObjectType):
    pk = graphene.ID()
    name = graphene.String()
    member_list = graphene.List(ContestTeamMemberType)
    approved = graphene.Boolean()
    owner = graphene.Field(UserType)

    def resolve_pk(self, info: ResolveInfo) -> graphene.ID:
        return self.pk

    def resolve_name(self, info: ResolveInfo) -> graphene.String:
        return self.name

    def resolve_member_list(self, info: ResolveInfo) -> graphene.List:
        return self.memeber.all()

    def resolve_approved(self, info: ResolveInfo) -> graphene.Boolean:
        return self.approved

    def resolve_owner(self, info: ResolveInfo):
        return self.owner


class ContestRankingMetaType(graphene.ObjectType):
    start_time = graphene.DateTime()

    def resolve_start_time(self, info: ResolveInfo):
        return self.settings.start_time


class ContestRankingType(graphene.ObjectType):
    submissions = graphene.List(ContestRankingSubmissionType)
