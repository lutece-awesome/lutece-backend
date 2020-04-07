import graphene
from annoying.functions import get_object_or_None
from django.core.paginator import Paginator
from graphql import ResolveInfo, GraphQLError

from article.constant import PER_PAGE_COUNT, COMMENT_PER_PAGE_COUNT
from article.models import HomeArticle, UserArticle, ArticleComment, Article
from article.type import HomeArticleType, UserArticleType, HomeArticleListType, UserArticleListType, ArticleCommentListType


class Query(object):
    user_article = graphene.Field(UserArticleType, pk=graphene.ID())
    user_article_list = graphene.Field(UserArticleListType, page=graphene.Int(), filter=graphene.String())
    home_article = graphene.Field(HomeArticleType, slug=graphene.ID())
    home_article_list = graphene.Field(HomeArticleListType, page=graphene.Int(), filter=graphene.String())
    article_comment_list = graphene.Field(ArticleCommentListType, pk=graphene.ID(), page=graphene.Int())

    def resolve_user_article(self: None, info: ResolveInfo, pk: int) -> UserArticle or None:
        ret = get_object_or_None(UserArticle, pk=pk)
        # if ret is None and been disabled and the request user do not have read permission, ignore
        # this request and return none
        if ret and ret.disable and not info.context.user.has_perm('article.view_userarticle'):
            return None
        return ret


    def resolve_user_article_list(self: None, info: ResolveInfo, page: int, filter: str) -> UserArticleListType:
        user_article_list = UserArticle.objects.all()
        privilege = info.context.user.has_perm('article.view_userarticle')
        if not privilege:
            user_article_list = user_article_list.filter(disable=False)
        if filter:
            user_article_list = user_article_list.filter(title__icontains=filter)
        user_article_list = user_article_list.order_by('-create_time')
        paginator = Paginator(user_article_list, PER_PAGE_COUNT)
        return UserArticleListType(max_page=paginator.num_pages, user_article_list=paginator.get_page(page))


    def resolve_home_article(self: None, info: ResolveInfo, slug: str) -> HomeArticle or None:
        ret = get_object_or_None(HomeArticle, slug=slug)
        # if ret is not None and been disabled and the request user do not have read permission, ignore
        # this request and return none
        if ret and ret.disable and not info.context.user.has_perm('article.view_homearticle'):
            return None
        return ret

    def resolve_home_article_list(self: None, info: ResolveInfo, page: int, filter: str) -> HomeArticleListType:
        home_article_list = HomeArticle.objects.all()
        privilege = info.context.user.has_perm('article.view_homearticle')
        if not privilege:
            home_article_list = home_article_list.filter(disable=False)
        if filter:
            home_article_list = home_article_list.filter(title__icontains=filter)
        home_article_list = home_article_list.order_by('-create_time')
        paginator = Paginator(home_article_list, PER_PAGE_COUNT)
        return HomeArticleListType(max_page=paginator.num_pages, home_article_list=paginator.get_page(page))

    def resolve_article_comment_list(self: None, info: ResolveInfo, pk: int, page: int) -> ArticleCommentListType:
        article = get_object_or_None(Article, pk=pk)
        if not article:
            raise GraphQLError('No such article')
        article_comment_list = ArticleComment.objects.filter(article=article)
        privilege = info.context.user.has_perm('article.view_articlecomment')
        if not privilege:
            article_comment_list = article_comment_list.filter(disable=False)
        article_comment_list = article_comment_list.order_by('-vote')
        paginator = Paginator(article_comment_list, COMMENT_PER_PAGE_COUNT)
        return ArticleCommentListType(max_page=paginator.num_pages, article_comment_list=paginator.get_page(page))
