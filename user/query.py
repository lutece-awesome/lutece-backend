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

    def resolve_user(self: None, info: ResolveInfo, username) -> User:
        return User.objects.get(username=username)

    def resolve_user_list(self: None, info: ResolveInfo, page: int, filter: str) -> UserListType:
        request_usr = info.context.user
        user_list = User.objects.all().order_by('-solved')
        if not request_usr.has_perm('user.view'):
            user_list = user_list.filter(is_active=True, is_staff=False)
        if filter:
            user_list = user_list.filter(username__icontains=filter)
        paginator = Paginator(user_list, PER_PAGE_COUNT)
        return UserListType(max_page=paginator.num_pages, user_list=paginator.get_page(page))

    '''
        Search the matching user of the specific filter.
        Nothing would return if there is no filter(to avoid the empty filter situation).
    '''
    def resolve_user_search(self: None, info: ResolveInfo, filter: str) -> UserListType:
        user_list = User.objects.all()
        if not info.context.user.has_perm('user.view'):
            user_list = user_list.filter(is_staff=False)
        if filter:
            user_list = user_list.filter(username__icontains=filter)
        else:
            user_list = []
        return UserListType(max_page=1, user_list=user_list[:5])
