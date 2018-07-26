import graphene
from graphene_django.types import DjangoObjectType
from .models import User
from annoying.functions import get_object_or_None
from graphql_jwt.shortcuts import get_token, get_payload
from .group import Group
from utils.schema import paginatorList
from json import dumps


class UserType(DjangoObjectType):
    class Meta:
        model = User
        only_fields = ('username', 'display_name', 'school', 'company',
                       'location', 'about', 'tried', 'solved')

    gravataremail = graphene.String()
    group = graphene.String()

    def resolve_gravataremail(self, info, * args, ** kwargs):
        return self.gravataremail

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
    payload = graphene.JSONString()

    def mutate(self, info, ** kwargs):
        from .form import UserLoginForm
        LoginForm = UserLoginForm(kwargs)
        if LoginForm.is_valid():
            values = LoginForm.cleaned_data
            user = User.objects.get(username=values['username'])
            token = get_token(user)
            payload = get_payload(token, info.context)
            return UserLogin(payload=dumps(payload), token=token)
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
    payload = graphene.JSONString()

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
            return Register(payload=dumps(get_payload), token=token)
        else:
            raise RuntimeError(SignupForm.errors.as_json())


class Query(object):

    user = graphene.Field(UserType, pk=graphene.ID())
    userList = graphene.Field(UserListType, page=graphene.Int())

    def resolve_user(self, info, pk):
        return User.objects.get(pk=pk)

    def resolve_userList(self, info, page):
        from django.core.paginator import Paginator
        from Lutece.config import PER_PAGE_COUNT
        userlist = User.objects.all().order_by('-solved').filter(show=True)
        paginator = Paginator(userlist, PER_PAGE_COUNT)
        return UserListType(maxpage=paginator.num_pages, userList=paginator.get_page(page))


class Mutation(graphene.AbstractType):
    register = Register.Field()
    user_login = UserLogin.Field()
