import graphene
from graphene_django.types import DjangoObjectType
from annoying.functions import get_object_or_None
from .models import Article, ArticleDiscussion
from user.schema import UserType
from user.models import User
from graphql_jwt.decorators import login_required
from .form import BasicArticleForm
from utils.schema import PaginatorList
from discussion.schema import DiscussionType


class ArticleType(DjangoObjectType):
    class Meta:
        model = Article
        only_fields = ('id', 'title', 'content', 'create_time',
                       'slug', 'view', 'vote', 'disable')

    author = graphene.Field(UserType)

    def resolve_user(self, info, * args, ** kwargs):
        return self.user


class ArticleDiscussionType(graphene.ObjectType, DiscussionType):
    pass


class ArticleDiscussionListType(graphene.ObjectType):
    class Meta:
        interfaces = (PaginatorList, )
    discussionList = graphene.List(ArticleDiscussionType)


class ArticleListType(graphene.ObjectType):
    class Meta:
        interfaces = (PaginatorList, )

    articleList = graphene.List(ArticleType)


class CreateArticle(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        content = graphene.String(required=True)

    state = graphene.Boolean()

    @login_required
    def mutate(self, info, * args, ** kwargs):
        ArticleForm = BasicArticleForm(kwargs)
        if ArticleForm.is_valid():
            values = ArticleForm.cleaned_data
            Article(
                title=values['title'],
                content=values['content'],
                user=info.context.user,
            ).save()
            return CreateArticle(state=True)
        else:
            raise RuntimeError(ArticleForm.errors.as_json())


class Query(object):
    article = graphene.Field(ArticleType, slug=graphene.String())
    articleList = graphene.Field(ArticleListType, page=graphene.Int())
    articleDiscussionList = graphene.Field(ArticleDiscussionListType, slug=graphene.String(
    ), page=graphene.Int(), time=graphene.Int(required=False))

    def resolve_article(self, info, slug):
        s = Article.objects.get(slug=slug)
        if s.disable and not info.context.user.has_perm('article.view_all'):
            return None
        return s

    def resolve_articleList(self, info, page):
        from django.core.paginator import Paginator
        resultList = Article.objects.all()
        if not info.context.user.has_perm('article.view_all'):
            resultList = resultList.filter(disable=False)
        paginator = Paginator(resultList, 10)
        return ArticleListType(maxpage=paginator.num_pages, articleList=paginator.get_page(page))

    def resolve_articleDiscussionList(self, info, slug, page, * args, ** kwargs):
        from django.core.paginator import Paginator
        discussionList = ArticleDiscussion.objects.filter(
            article=Article.objects.get(slug=slug), reply=None).order_by('submit_time')
        if not info.context.user.has_perm('article.view_all'):
            discussionList = discussionList.filter(visibility=True)
        paginator = Paginator(discussionList, 10)
        return ArticleDiscussionListType(maxpage=paginator.num_pages, discussionList=paginator.get_page(page))


class Mutation(graphene.AbstractType):
    CreateArticle = CreateArticle.Field()
