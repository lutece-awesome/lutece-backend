import graphene
from django_gravatar.helpers import get_gravatar_url
from graphene_django.types import DjangoObjectType
from graphql import ResolveInfo

from user.attachinfo.models import AttachInfo


class UserAttachInfoType(DjangoObjectType):
    class Meta:
        model = AttachInfo
        only_fields = ('school', 'company', 'location', 'about', 'codeforces', 'atcoder')

    gravatar = graphene.String()

    def resolve_gravatar(self, info: ResolveInfo) -> str:
        return get_gravatar_url(self.user.email, size=250)
