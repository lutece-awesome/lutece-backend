import graphene
from graphene_django import DjangoObjectType
from graphql import ResolveInfo

from article.models import ArticleRecord
from user.type import UserType
from utils.interface import PaginatorList


class ArticleRecordType(DjangoObjectType):
    class Meta:
        model = ArticleRecord
        only_fields = ('count',)


class ArticleType(graphene.ObjectType):
    pk = graphene.ID()
    title = graphene.String()
    author = graphene.Field(UserType)
    content = graphene.String()
    create_time = graphene.DateTime()
    last_update_time = graphene.DateTime()
    record = graphene.Field(ArticleRecordType)

    def resolve_pk(self, info: ResolveInfo) -> graphene.ID():
        return self.pk

    def resolve_title(self, info: ResolveInfo) -> graphene.String():
        return self.title

    def resolve_author(self, info: ResolveInfo) -> graphene.String():
        return self.author

    def resolve_content(self, info: ResolveInfo) -> graphene.String():
        return self.content

    def resolve_create_time(self, info: ResolveInfo) -> graphene.DateTime():
        return self.create_time

    def resolve_last_update_time(self, info: ResolveInfo) -> graphene.DateTime():
        return self.last_update_time

    def resolve_record(self, info: ResolveInfo) -> ArticleRecordType:
        return self.record


class HomeArticleType(ArticleType):
    slug = graphene.String()
    preview = graphene.String()
    rank = graphene.Int()

    def resolve_slug(self, info: ResolveInfo) -> graphene.String():
        return self.slug

    def resolve_preview(self, info: ResolveInfo) -> graphene.String():
        return self.preview

    def resolve_rank(self, info: ResolveInfo) -> graphene.Int():
        return self.rank


class UserArticleType(ArticleType):
    pass


class HomeArticleListType(graphene.ObjectType, interfaces=[PaginatorList]):
    home_article_list = graphene.List(HomeArticleType, )
