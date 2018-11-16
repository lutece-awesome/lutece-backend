import graphene
from datetime import datetime, date
from django.db.models import Q
from graphql import ResolveInfo

from user.attachinfo.type import UserAttachInfoType
from user.models import User
from user.statistics.type import UserSubmissionStatisticsType
from utils.interface import PaginatorList


class UserRankType(graphene.ObjectType):
    position = graphene.Int()
    count = graphene.Int()
    solve = graphene.JSONString()

    __slots__ = {
        'user'
    }

    def __init__(self, user: User, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def resolve_position(self, info: ResolveInfo) -> int:
        return User.objects.filter(is_staff=False).filter(
            Q(solved__gt=self.user.solved) | Q(solved__exact=self.user.solved, pk__lt=self.user.pk)).count() + 1

    def resolve_count(self, info: ResolveInfo) -> int:
        return User.objects.filter(is_staff=False).count()


class UserType(graphene.ObjectType):
    pk = graphene.ID()
    username = graphene.String()
    joined_date = graphene.Date()
    last_login_date = graphene.DateTime()
    attach_info = graphene.Field(UserAttachInfoType)
    solved = graphene.Int()
    tried = graphene.Int()
    rank = graphene.Field(UserRankType)
    statistics = graphene.Field(UserSubmissionStatisticsType)

    def resolve_pk(self, info: ResolveInfo) -> graphene.ID:
        return self.pk

    def resolve_username(self, info: ResolveInfo) -> graphene.String:
        return self.username

    def resolve_joined_date(self: User, info: ResolveInfo) -> date:
        return self.date_joined.date()

    def resolve_last_login_date(self: User, info: ResolveInfo) -> datetime:
        return self.last_login or self.date_joined

    def resolve_attach_info(self, info: ResolveInfo) -> graphene.Field(UserAttachInfoType):
        return self.attach_info

    def resolve_solved(self, info: ResolveInfo) -> graphene.Int:
        return self.solved

    def resolve_tried(self, info: ResolveInfo) -> graphene.Int:
        return self.tried

    def resolve_rank(self: User, info: ResolveInfo) -> UserRankType:
        return UserRankType(user=self)

    def resolve_statistics(self, info: ResolveInfo) -> graphene.Field(UserSubmissionStatisticsType):
        return UserSubmissionStatisticsType(user=self)


class UserListType(graphene.ObjectType, interfaces=[PaginatorList]):
    user_list = graphene.List(UserType)
