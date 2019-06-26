import graphene
from annoying.functions import get_object_or_None
from graphql import ResolveInfo

from reply.constant import REPLY_COMMENT_PER_PAGE_COUNT
from reply.models import BaseReply, ReplyVote
from user.type import UserType


class AbstractBaseReplyType(graphene.ObjectType):
    pk = graphene.ID()
    content = graphene.String()
    author = graphene.Field(UserType)
    create_time = graphene.DateTime()
    last_update_time = graphene.DateTime()
    vote = graphene.Int()
    self_attitude = graphene.Boolean()
    total_reply_number = graphene.Int()

    def resolve_pk(self, info: ResolveInfo) -> graphene.ID():
        return self.pk

    def resolve_content(self, info: ResolveInfo) -> graphene.String():
        return self.content

    def resolve_author(self, info: ResolveInfo) -> UserType:
        return self.author

    def resolve_create_time(self, info: ResolveInfo) -> graphene.DateTime():
        return self.create_time

    def resolve_last_update_time(self, info: ResolveInfo) -> graphene.DateTime():
        return self.last_update_time

    def resolve_vote(self, info: ResolveInfo) -> graphene.Int():
        return self.vote

    def resolve_self_attitude(self, info: ResolveInfo) -> graphene.Boolean():
        usr = info.context.user
        if not usr.is_authenticated:
            return False
        vote = get_object_or_None(ReplyVote, reply=self, record_user=usr)
        return vote.attitude if vote else False

    def resolve_total_reply_number(self, info: ResolveInfo) -> graphene.Int():
        return BaseReply.objects.filter(ancestor=self).count()


class BaseReplyType(AbstractBaseReplyType):
    reply = graphene.List(AbstractBaseReplyType)

    def resolve_reply(self, info: ResolveInfo) -> lambda: AbstractBaseReplyType:
        return BaseReply.objects.filter(ancestor=self).order_by('-vote')[:REPLY_COMMENT_PER_PAGE_COUNT]
