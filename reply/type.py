import graphene
from graphql import ResolveInfo

from user.type import UserType


class BaseReplyType(graphene.ObjectType):
    pk = graphene.ID()
    content = graphene.String()
    author = graphene.Field(UserType)
    reply = graphene.ObjectType(lambda: BaseReplyType)
    create_time = graphene.DateTime()

    def resolve_pk(self, info: ResolveInfo) -> graphene.ID():
        return self.pk

    def resolve_content(self, info: ResolveInfo) -> graphene.String():
        return self.content

    def resolve_author(self, info: ResolveInfo) -> UserType:
        return self.author

    def resolve_reply(self, info: ResolveInfo) -> lambda: BaseReplyType:
        return self.reply

    def resolve_create_time(self, info: ResolveInfo) -> graphene.DateTime():
        return self.create_time
