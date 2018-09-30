import graphene
from user.models import User
from graphql_jwt.shortcuts import get_token, get_payload, get_user_by_payload
from utils.schema import paginatorList
from graphene.types.generic import GenericScalar
from graphql_jwt.decorators import login_required
from graphql_jwt.mixins import RefreshMixin
from graphql_jwt.mutations import JSONWebTokenMixin
from django_gravatar.helpers import get_gravatar_url
from user.attachinfo import AttachInfoTypeMixin
# from submission.schema import SubmissionStatistics


class UserType( graphene.ObjectType ):
    username = graphene.String()
    gravataremail = graphene.String()
    joined_date = graphene.Date()
    lastlogin_date = graphene.DateTime()
    gravatar = graphene.String()
    attach_info = graphene.Field( AttachInfoTypeMixin )

    def resolve_username( self , info , * args , ** kwargs ):
        return self.username

    def resolve_joined_date( self , info , * args , ** kwargs ):
        return self.date_joined.date()
    
    def resolve_lastlogin_date( self , info , * args , ** kwargs ):
        return self.last_login or self.date_joined
    
    def resolve_gravatar( self , info , * args , ** kwargs ):
        return get_gravatar_url( self.email , size = 250 )
    
    def resolve_attach_info( self , info , * args , ** kwargs ):
        return self.attach_info
        
class UserListType(graphene.ObjectType):
    class Meta:
        interfaces = (paginatorList, )
    userList = graphene.List(UserType)

class UserLogin(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)

    token = graphene.String()
    payload = GenericScalar()
    permission = GenericScalar()
    user = graphene.Field(UserType)

    def mutate(self, info, ** kwargs):
        from .form import UserLoginForm
        from django.contrib.auth.models import update_last_login

        LoginForm = UserLoginForm(kwargs)
        if LoginForm.is_valid():
            values = LoginForm.cleaned_data
            user = User.objects.get( username = values['username'] )
            token = get_token(user)
            payload = get_payload(token, info.context)
            update_last_login( None , user )
            return UserLogin( payload = payload, token = token, permission = list( user.get_all_permissions() ), user = user )
        else:
            raise RuntimeError(LoginForm.errors.as_json())


class UserTokenRefresh(JSONWebTokenMixin,
                       RefreshMixin,
                       graphene.Mutation):
    permission = GenericScalar()
    user = graphene.Field(UserType)

    @classmethod
    def mutate(cls, *arg, **kwargs):
        result = cls.refresh(*arg, **kwargs)
        user = get_user_by_payload(result.payload)
        result.user = user
        result.permission = list(user.get_all_permissions())
        return result

class Register(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)
        display_name = graphene.String(required=True)
        school = graphene.String()
        company = graphene.String()
        location = graphene.String()

    token = graphene.String()
    payload = GenericScalar()
    permission = GenericScalar()
    user = graphene.Field(UserType)

    def mutate(self, info, ** kwargs):
        from .form import UserSignupForm
        SignupForm = UserSignupForm(kwargs)
        if SignupForm.is_valid():
            values = SignupForm.cleaned_data
            new_user = User(
                username=values['username'],
                email=values['email'],
                display_name=values['display_name'],
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
            return Register(payload=payload, token=token, permission=list(new_user.get_all_permissions()), user=new_user)
        else:
            raise RuntimeError(SignupForm.errors.as_json())


class Query(object):

    userList = graphene.Field(
        UserListType, page=graphene.Int(), filter=graphene.String())
    userSearch = graphene.Field(UserListType, filter=graphene.String())
    user = graphene.Field(UserType, username=graphene.String())
    topUser = graphene.List( UserType , number=graphene.Int())

    def resolve_userList(self, info, page, **kwargs):
        from django.core.paginator import Paginator
        from Lutece.config import PER_PAGE_COUNT
        filter = kwargs.get('filter')
        user_list = User.objects.all().order_by('-solved').filter(show=True)
        if filter is not None:
            user_list = user_list.filter(Q(display_name__icontains=filter) | Q(
                school__icontains=filter) | Q(company__icontains=filter) | Q(location__icontains=filter))
        paginator = Paginator(user_list, PER_PAGE_COUNT)
        return UserListType(maxpage=paginator.num_pages, userList=paginator.get_page(page))

    def resolve_userSearch(self, info, **kwargs):
        filter = kwargs.get('filter')
        user_list = User.objects.all().filter(show=True)
        if filter is not None:
            user_list = user_list.filter(display_name__icontains=filter)
        return UserListType(maxpage=1, userList=user_list[:5])

    def resolve_user(self, info, username):
        return User.objects.get(username=username)
    
    def resolve_topUser(self, info, number):
        return User.objects.filter( show = True ).order_by( '-solved' )[:number]


class Mutation(graphene.AbstractType):
    register = Register.Field()
    user_login = UserLogin.Field()
    UserInfoUpdate = UserInfoUpdate.Field()
    UserTokenRefresh = UserTokenRefresh.Field()
