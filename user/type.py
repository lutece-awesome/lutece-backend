import graphene
from django.db.models import Q

from user.attachinfo.type import UserAttachInfoType
from user.models import User
from user.statistics.type import UserSubmissionStatisticsType
from utils.interface import PaginatorList


class UserRankType(graphene.ObjectType):
    position = graphene.Int()
    count = graphene.Int()
    solve = graphene.JSONString()

    def __init__(self, *args, **kwargs):
        if 'user' in kwargs:
            self.user = kwargs['user']
        else:
            raise RuntimeError('User field is required')

    def resolve_position(self, info, *args, **kwargs):
        return User.objects.filter(is_staff=False).filter(
            Q(solved__gt=self.user.solved) | Q(solved__exact=self.user.solved, pk__lt=self.user.pk)).count() + 1

    def resolve_count(self, info, *args, **kwargs):
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

    def resolve_pk(self, info, *args, **kwargs):
        return self.pk

    def resolve_username(self, info, *args, **kwargs):
        return self.username

    def resolve_joined_date(self, info, *args, **kwargs):
        return self.date_joined.date()

    def resolve_last_login_date(self, info, *args, **kwargs):
        return self.last_login or self.date_joined

    def resolve_attach_info(self, info, *args, **kwargs):
        return self.attach_info

    def resolve_solved(self, info, *args, **kwargs):
        return self.solved

    def resolve_tried(self, info, *args, **kwargs):
        return self.tried

    def resolve_rank(self, info, *args, **kwargs):
        return UserRankType(user=self)

    def resolve_statistics(self, info, *args, **kwargs):
        return UserSubmissionStatisticsType(user=self)


class UserListType(graphene.ObjectType):
    class Meta:
        interfaces = (PaginatorList,)

    user_list = graphene.List(UserType)
