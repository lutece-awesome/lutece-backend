import graphene
from graphql import ResolveInfo
from graphql_jwt.decorators import permission_required

from contest.models import ContestProblem
from problem.type import ProblemType


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

    @permission_required('contest.view')
    def resolve_password(self, info: ResolveInfo) -> graphene.String():
        return self.password


class ContestType(graphene.ObjectType):
    title = graphene.String()
    settings = graphene.Field(ContestSettingsType)
    problem_list = graphene.List(ProblemType)

    def resolve_title(self, info: ResolveInfo) -> graphene.String():
        return self.title

    def resolve_settings(self, info: ResolveInfo) -> ContestSettingsType:
        return self.settings

    def resolve_problem_list(self, info: ResolveInfo) -> graphene.List(ProblemType):
        return map(lambda x: x.problem, ContestProblem.objects.filter(contest=self))
