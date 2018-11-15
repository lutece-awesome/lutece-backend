import graphene
from django.core.paginator import Paginator
from graphql import ResolveInfo

from user.constant import PER_PAGE_COUNT
from user.models import User
from user.type import UserType, UserListType


class Query(object):
    user = graphene.Field(UserType, username=graphene.String())
    user_list = graphene.Field(UserListType, filter=graphene.String(), page=graphene.Int())
    user_search = graphene.Field(UserListType, filter=graphene.String())

    def resolve_user(self, info: ResolveInfo, username) -> User:
        return User.objects.get(username=username)

    def resolve_user_list(self, info: ResolveInfo, page, filter) -> UserListType:
        request_usr = info.context.user
        user_list = User.objects.all().order_by('-solved')
        if not request_usr.has_perm('user.view'):
            user_list = user_list.filter(is_active=True, is_staff=False)
        if filter:
            user_list = user_list.filter(username__icontains=filter)
        paginator = Paginator(user_list, PER_PAGE_COUNT)
        return UserListType(maxpage=paginator.num_pages, user_list=paginator.get_page(page))

    def resolve_user_search(self, info: ResolveInfo, filter) -> UserListType:
        user_list = User.objects.all()
        if not info.context.user.has_perm('user.view'):
            user_list = user_list.filter(is_staff=False)
        if filter:
            user_list = user_list.filter(username__icontains=filter)
        return UserListType(maxpage=1, user_list=user_list[:5])
