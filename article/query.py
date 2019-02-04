import graphene
from annoying.functions import get_object_or_None
from django.core.paginator import Paginator
from graphql import ResolveInfo

from article.constant import PER_PAGE_COUNT
from article.models import HomeArticle, UserArticle
from article.type import HomeArticleType, UserArticleType, HomeArticleListType


class Query(object):
    user_article = graphene.Field(UserArticleType, pk=graphene.ID())
    home_article = graphene.Field(HomeArticleType, slug=graphene.ID())
    home_article_list = graphene.Field(HomeArticleListType, page=graphene.Int(), filter=graphene.String())

    def resolve_user_article(self: None, info: ResolveInfo, pk: int) -> UserArticle or None:
        ret = get_object_or_None(UserArticle, pk=pk)
        # if ret is None and been disabled and the request user do not have read permission, ignore
        # this request and return none
        if ret and ret.disable and not info.context.user.has_perm('article.view_userarticle'):
            return None
        return ret

    def resolve_home_article(self: None, info: ResolveInfo, slug: str) -> HomeArticle or None:
        ret = get_object_or_None(HomeArticle, slug=slug)
        # if ret is not None and been disabled and the request user do not have read permission, ignore
        # this request and return none
        if ret and ret.disable and not info.context.user.has_perm('article.view_homearticle'):
            return None
        return ret

    def resolve_home_article_list(self: None, info: ResolveInfo, page: int, filter: str) -> HomeArticleListType:
        home_article_list = HomeArticle.objects.all()
        privileage = info.context.user.has_perm('article.view_homearticle')
        if not privileage:
            home_article_list = home_article_list.filter(disable=False)
        if filter:
            home_article_list = home_article_list.filter(title__icontains=filter)
        paginator = Paginator(home_article_list, PER_PAGE_COUNT)
        return HomeArticleListType(maxpage=paginator.num_pages, home_article_list=paginator.get_page(page))
