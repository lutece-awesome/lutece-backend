import graphene
from django.core.paginator import Paginator

from user.constant import PER_PAGE_COUNT
from user.models import User
from user.type import UserType, UserListType


class Query(object):
    user = graphene.Field(UserType, username=graphene.String())
    user_list = graphene.Field(UserListType, filter=graphene.String(), page=graphene.Int())
    user_search = graphene.Field(UserListType, filter=graphene.String())

    def resolve_user(self, info, *args, **kwargs):
        return User.objects.get(username=kwargs.get('username'))

    def resolve_user_list(self, info, *args, **kwargs):
        page = kwargs.get('page')
        filter = kwargs.get('filter')
        user_list = User.objects.all().filter(is_active=True, is_staff=False).order_by('-solved')
        if filter:
            user_list = user_list.filter(username__icontains=filter)
        paginator = Paginator(user_list, PER_PAGE_COUNT)
        return UserListType(maxpage=paginator.num_pages, user_list=paginator.get_page(page))

    def resolve_user_search(self, info, *args, **kwargs):
        filter = kwargs.get('filter')
        user_list = User.objects.all()
        if not info.context.user.has_perm('user.view'):
            user_list = user_list.filter(is_staff=False)
        if filter:
            user_list = user_list.filter(username__icontains=filter)
        return UserListType(maxpage=1, user_list=user_list[:5])
