import graphene
from django.contrib.auth.models import update_last_login
from graphene.types.generic import GenericScalar
from graphql import ResolveInfo
from graphql_jwt.decorators import login_required
from graphql_jwt.mixins import RefreshMixin
from graphql_jwt.mutations import JSONWebTokenMixin
from graphql_jwt.shortcuts import get_token, get_payload, get_user_by_payload

from user.attachinfo.models import AttachInfo
from user.form import UserLoginForm, UserSignupForm, UserAttachInfoUpdateForm
from user.models import User
from user.type import UserType
from utils.function import assign


class UserLogin(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)

    token = graphene.String()
    payload = GenericScalar()
    permission = GenericScalar()
    user = graphene.Field(UserType)

    def mutate(self, info: ResolveInfo, **kwargs):
        login_form = UserLoginForm(kwargs)
        if login_form.is_valid():
            values = login_form.cleaned_data
            usr = User.objects.get(username=values.get('username'))
            token = get_token(usr)
            payload = get_payload(token, info.context)
            update_last_login(None, usr)
            return UserLogin(payload=payload, token=token, permission=list(usr.get_all_permissions()), user=usr)
        else:
            raise RuntimeError(login_form.errors.as_json())


class UserTokenRefresh(JSONWebTokenMixin, RefreshMixin, graphene.Mutation):
    permission = GenericScalar()
    user = graphene.Field(UserType)

    @classmethod
    def mutate(cls, *arg, **kwargs):
        result = cls.refresh(*arg, **kwargs)
        user = get_user_by_payload(result.payload)
        result.user = user
        result.permission = list(user.get_all_permissions())
        return result


class UserRegister(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)
        school = graphene.String()
        company = graphene.String()
        location = graphene.String()
        about = graphene.String()

    token = graphene.String()
    payload = GenericScalar()
    permission = GenericScalar()
    user = graphene.Field(UserType)

    def mutate(self, info: ResolveInfo, **kwargs):
        signup_form = UserSignupForm(kwargs)
        if signup_form.is_valid():
            values = signup_form.cleaned_data
            usr = User()
            attach_info = AttachInfo()
            assign(usr, **values)
            assign(attach_info, **values)
            usr.set_password(usr.password)
            attach_info.save()
            usr.attach_info = attach_info
            usr.save()
            token = get_token(usr)
            payload = get_payload(token, info.context)
            return UserRegister(payload=payload, token=token, permission=list(usr.get_all_permissions()), user=usr)
        else:
            raise RuntimeError(signup_form.errors.as_json())


class UserAttachInfoUpdate(graphene.Mutation):
    class Arguments:
        about = graphene.String(required=True)
        school = graphene.String(required=True)
        company = graphene.String(required=True)
        location = graphene.String(required=True)
        # gravatar = graphene.String( required = True )

    state = graphene.Boolean()

    @login_required
    def mutate(self, info: ResolveInfo, **kwargs):
        update_form = UserAttachInfoUpdateForm(kwargs)
        if update_form.is_valid():
            values = update_form.cleaned_data
            usr = info.context.user
            assign(usr.attach_info, **values)
            usr.attach_info.save()
            return UserAttachInfoUpdate(state=True)
        else:
            raise RuntimeError(update_form.errors.as_json())


class Mutation(graphene.AbstractType):
    user_register = UserRegister.Field()
    user_login = UserLogin.Field()
    user_token_refresh = UserTokenRefresh.Field()
    user_attach_info_update = UserAttachInfoUpdate.Field()
