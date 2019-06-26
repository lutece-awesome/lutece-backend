import graphene
from django.core.paginator import Paginator
from graphql import ResolveInfo

from reply.constant import REPLY_COMMENT_PER_PAGE_COUNT
from reply.models import BaseReply
from reply.type import AbstractBaseReplyType


class Query(object):
    comment_reply_list = graphene.List(AbstractBaseReplyType, pk=graphene.ID(), page=graphene.Int())

    def resolve_comment_reply_list(self: None, info: ResolveInfo, pk: int, page: int):
        return Paginator(
            BaseReply.objects.filter(ancestor=BaseReply.objects.get(pk=pk), disable=False).order_by('-vote'),
            REPLY_COMMENT_PER_PAGE_COUNT).get_page(page)
