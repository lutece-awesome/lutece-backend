import graphene
from graphene_django.types import DjangoObjectType
from .models import User
from annoying.functions import get_object_or_None
from graphql_jwt.shortcuts import get_token, get_payload
from .group import Group
from utils.schema import paginatorList
from json import dumps
from graphene.types.generic import GenericScalar


class UserType(DjangoObjectType):
    class Meta:
        model = User
        only_fields = ('username', 'display_name', 'school', 'company',
                       'location', 'about', 'tried', 'solved')

    gravataremail = graphene.String()
    group = graphene.String()

    def resolve_group(self, info, * args,  ** kwargs):
        return Group.get_user_group(self.group).value.display


class UserListType(graphene.ObjectType):
    class Meta:
        interfaces = (paginatorList, )
    userList = graphene.List(UserType)


class UserLogin(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)

    token = graphene.String()
    permission = graphene.String()
    payload = GenericScalar()

    def mutate(self, info, ** kwargs):
        from .form import UserLoginForm
        LoginForm = UserLoginForm(kwargs)
        if LoginForm.is_valid():
            values = LoginForm.cleaned_data
            user = User.objects.get(username=values['username'])
            token = get_token(user)
            payload = get_payload(token, info.context)
            return UserLogin(payload=payload, token=token, permission=dumps(list(user.get_all_permissions())))
        else:
            raise RuntimeError(LoginForm.errors.as_json())


class Register(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)
        displayname = graphene.String(required=True)
        school = graphene.String()
        company = graphene.String()
        location = graphene.String()

    token = graphene.String()
    payload = GenericScalar()

    def mutate(self, info, ** kwargs):
        from .form import UserSignupForm
        SignupForm = UserSignupForm(kwargs)
        if SignupForm.is_valid():
            values = SignupForm.cleaned_data
            new_user = User(
                username=values['username'],
                email=values['email'],
                display_name=values['displayname'],
                school=values['school'],
                company=values['company'],
                location=values['location'],
                is_staff=False,
                is_superuser=False,)
            new_user.set_password(values['password'])
            new_user.save()
            new_user.set_group(Group.NORMAL_USER)
            token = get_token(new_user)
            payload = get_payload(token, info.context)
            return Register(payload=payload, token=token)
        else:
            raise RuntimeError(SignupForm.errors.as_json())


class Query(object):

    user = graphene.Field(UserType, username=graphene.String())
    userList = graphene.Field(
        UserListType, page=graphene.Int(), filter=graphene.String())
    userSearch = graphene.Field(UserListType, filter=graphene.String())
    userHeatmapData = graphene.String(username=graphene.String())

    def resolve_user(self, info, username):
        return User.objects.get(username=username)

    def resolve_userList(self, info, page, **kwargs):
        from django.core.paginator import Paginator
        from Lutece.config import PER_PAGE_COUNT
        filter = kwargs.get('filter')
        user_list = User.objects.all().order_by('-solved').filter(show=True)
        if filter is not None:
            user_list = user_list.filter(display_name__icontains=filter)
        paginator = Paginator(user_list, PER_PAGE_COUNT)
        return UserListType(maxpage=paginator.num_pages, userList=paginator.get_page(page))

    def resolve_userSearch(self, info, **kwargs):
        filter = kwargs.get('filter')
        user_list = User.objects.all().filter(show=True)
        if filter is not None:
            user_list = user_list.filter(display_name__icontains=filter)
        return UserListType(maxpage=1, userList=user_list[:5])

    def resolve_userHeatmapData(self, info, username):
        import datetime
        import time
        from json import dumps
        from submission.models import Submission
        from user.models import User
        now = datetime.datetime.now()
        start_date = now - datetime.timedelta(days=366)
        user = User.objects.get(username=username)
        s = Submission.objects.filter(
            user=user, submit_time__date__gt=start_date)
        ret = dict()
        for each in s:
            key = str(each.submit_time.strftime("%Y-%m-%d"))
            if key not in ret:
                ret[key] = 0
            ret[key] += 1
        return dumps([{'date': key, 'count': value} for key, value in ret.items()])


class Mutation(graphene.AbstractType):
    register = Register.Field()
    user_login = UserLogin.Field()
