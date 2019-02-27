import graphene
from annoying.functions import get_object_or_None
from graphql import ResolveInfo
from graphql_jwt.decorators import permission_required

from contest.models import ContestTeamMember


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
    registered = graphene.Boolean()

    def resolve_title(self, info: ResolveInfo) -> graphene.String():
        return self.title

    def resolve_settings(self, info: ResolveInfo) -> ContestSettingsType:
        return self.settings

    def resolve_registered(self, info: ResolveInfo) -> graphene.Boolean():
        usr = info.context.user
        return usr.has_perm('contest.view') or get_object_or_None(ContestTeamMember, user=usr,
                                                                  contest_team__contest=self)


# This is the duck type of Submission
class ContestRankingType(graphene.ObjectType):
    status = graphene.String()
    create_time = graphene.DateTime()

    def resolve_status(self, info: ResolveInfo) -> graphene.String():
        return self.status.full

    def resolve_create_time(self, info: ResolveInfo) -> graphene.String():
        return self.create_time


class ContestRankingGroupType(graphene.ObjectType):
    group_name = graphene.String()
    team_ranking_list = graphene.List(ContestRankingType)

    def resolve_group_name(self, info: ResolveInfo) -> graphene.String():
        return self.group_name

    def resolve_team_ranking_list(self, info: ResolveInfo) -> graphene.List(ContestRankingType):
        return self.team_ranking_list
