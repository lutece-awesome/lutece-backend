import graphene
from graphene_django.types import DjangoObjectType
from .models import User
from annoying.functions import get_object_or_None
from graphql_jwt.shortcuts import get_token, get_payload, get_user_by_payload
from .group import Group
from utils.schema import paginatorList
from graphene.types.generic import GenericScalar
from graphql_jwt.decorators import login_required
from graphql_jwt.mixins import RefreshMixin
from graphql_jwt.mutations import JSONWebTokenMixin
from django.db.models import Q, Count
from django.db.models.functions import TruncDate, Cast
from django.db.models.fields import CharField
from submission.schema import SubmissionStatistics


class UserType(DjangoObjectType):
    class Meta:
        model = User
        only_fields = ('username', 'display_name', 'school', 'company',
                       'location', 'about', 'tried', 'solved')

    gravataremail = graphene.String()
    group = graphene.String()
    heatmap = GenericScalar()
    analysis = GenericScalar()
    joined_date = graphene.Date()
    lastlogin_date = graphene.DateTime()
    submission_statistics = graphene.Field( SubmissionStatistics )

    def resolve_joined_date( self , info , * args , ** kwargs ):
        return self.date_joined.date()
    
    def resolve_lastlogin_date( self , info , * args , ** kwargs ):
        return self.last_login or self.date_joined

    def resolve_group(self, info, * args,  ** kwargs):
        return Group.get_user_group(self.group).value.display
    
    def resolve_submission_statistics( self , info , * args , ** kwargs ):
        return SubmissionStatistics( user = self )

    def resolve_heatmap(self, info, * args, ** kwargs):
        import datetime
        import time
        from submission.models import Submission
        from user.models import User
        now = datetime.datetime.now()
        start_date = now - datetime.timedelta(days=366)
        s = Submission.objects.filter(user=self, submit_time__date__gt=start_date)
        s = s.annotate(date=Cast(TruncDate('submit_time'), CharField()))
        s = s.order_by('date')
        s = s.values('date')
        s = s.annotate(count=Count('submission_id'))
        return list(s)

    def resolve_analysis(self, info, * args, ** kwargs):
        from submission.models import Submission
        from submission.judge_result import Judge_result
        s = Submission.objects.filter( user = self )
        privilege = info.context.user.has_perm('problem.view_all')
        if not privilege:
            s = Submission.objects.filter( problem__visible = True )
        solved = set()
        tried = set()
        trans = dict()
        for each in s:
            pk = each.problem.pk
            tried.add( pk )
            if pk not in trans:
                trans[pk] = each.problem.slug
            if Judge_result.get_judge_result(each.judge_status) is Judge_result.AC:
                solved.add( pk )
        return sorted([( each, 'yes' if each in solved else 'no' , trans[ each ] ) for each in tried], key=lambda x: x[0])


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
            return UserLogin(payload=payload, token=token, permission=list(user.get_all_permissions()), user=user)
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


class UserInfoUpdate(graphene.Mutation):
    class Arguments:
        display_name = graphene.String(required=True)
        school = graphene.String()
        company = graphene.String()
        location = graphene.String()
        about = graphene.String()

    state = graphene.Boolean()

    @login_required
    def mutate(self, info, ** kwargs):
        from .form import UserinfoForm
        userinfoForm = UserinfoForm(kwargs)
        user = info.context.user
        if userinfoForm.is_valid() and userinfoForm._clean(user.display_name):
            values = userinfoForm.cleaned_data
            display_name = values['display_name']
            school = values['school']
            company = values['company']
            location = values['location']
            about = values['about']
            user.display_name = display_name
            user.school = school
            user.company = company
            user.location = location
            user.about = about
            user.save()
            return UserInfoUpdate(state=True)
        else:
            raise RuntimeError(userinfoForm.errors.as_json())


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

    def resolve_userList(self, info, page, **kwargs):
        from django.core.paginator import Paginator
        filter = kwargs.get('filter')
        user_list = User.objects.all().order_by('-solved').filter(show=True)
        if filter is not None:
            user_list = user_list.filter(Q(display_name__icontains=filter) | Q(
                school__icontains=filter) | Q(company__icontains=filter) | Q(location__icontains=filter))
        paginator = Paginator(user_list, 12)
        return UserListType(maxpage=paginator.num_pages, userList=paginator.get_page(page))

    def resolve_userSearch(self, info, **kwargs):
        filter = kwargs.get('filter')
        user_list = User.objects.all().filter(show=True)
        if filter is not None:
            user_list = user_list.filter(display_name__icontains=filter)
        return UserListType(maxpage=1, userList=user_list[:5])

    def resolve_user(self, info, username):
        return User.objects.get(username=username)


class Mutation(graphene.AbstractType):
    register = Register.Field()
    user_login = UserLogin.Field()
    UserInfoUpdate = UserInfoUpdate.Field()
    UserTokenRefresh = UserTokenRefresh.Field()
