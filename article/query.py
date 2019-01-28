import graphene
from annoying.functions import get_object_or_None
from graphql import ResolveInfo

from article.models import HomeArticle, UserArticle
from article.type import HomeArticleType, UserArticleType


class Query(object):
    user_article = graphene.Field(UserArticleType, pk=graphene.ID())
    home_article = graphene.Field(HomeArticleType, pk=graphene.ID())

    def resolve_user_article(self: None, info: ResolveInfo, pk: int) -> UserArticle or None:
        ret = get_object_or_None(UserArticle, pk=pk)
        # if ret is None and been disabled and the request user do not have read permission, ignore
        # this request and return none
        if ret and ret.disable and not info.context.user.has_perm('article.view_userarticle'):
            return None
        return ret

    def resolve_home_article(self: None, info: ResolveInfo, pk: int) -> HomeArticle or None:
        ret = get_object_or_None(HomeArticle, pk=pk)
        # if ret is not None and been disabled and the request user do not have read permission, ignore
        # this request and return none
        if ret and ret.disable and not info.context.user.has_perm('article.view_homearticle'):
            return None
        return ret
