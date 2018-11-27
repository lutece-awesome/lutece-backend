import graphene
from annoying.functions import get_object_or_None
from graphql import ResolveInfo

from article.models import HomeArticle
from article.type import HomeArticleType


class Query(object):
    home_article = graphene.Field(HomeArticleType, pk=graphene.ID())

    def resolve_home_article(self: None, info: ResolveInfo, pk):
        ret = get_object_or_None(HomeArticle, pk=pk)
        if not ret or ret.disable:
            return None
        return ret
