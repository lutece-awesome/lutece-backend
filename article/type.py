import graphene
from annoying.functions import get_object_or_None
from graphene_django import DjangoObjectType
from graphql import ResolveInfo

from article.models import ArticleRecord, ArticleVote
from user.type import UserType
from utils.interface import PaginatorList
from reply.type import BaseReplyType


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
    vote = graphene.Int()
    self_attitude = graphene.Boolean()
    disable = graphene.Boolean()

    def resolve_pk(self, info: ResolveInfo) -> graphene.ID():
        return self.pk

    def resolve_title(self, info: ResolveInfo) -> graphene.String():
        return self.title

    def resolve_author(self, info: ResolveInfo) -> graphene.Field(UserType):
        return self.author

    def resolve_content(self, info: ResolveInfo) -> graphene.String():
        return self.content

    def resolve_create_time(self, info: ResolveInfo) -> graphene.DateTime():
        return self.create_time

    def resolve_last_update_time(self, info: ResolveInfo) -> graphene.DateTime():
        return self.last_update_time

    def resolve_record(self, info: ResolveInfo) -> ArticleRecordType:
        return self.record

    def resolve_vote(self, info: ResolveInfo) -> graphene.Int():
        return ArticleVote.objects.filter(article=self, attitude=True).count()

    def resolve_self_attitude(self, info: ResolveInfo) -> graphene.Boolean():
        usr = info.context.user
        if not usr.is_authenticated:
            return False
        vote = get_object_or_None(ArticleVote, article=self, record_user=usr)
        return vote.attitude if vote else False

    def resolve_disable(self, info: ResolveInfo) -> graphene.Boolean():
        return self.disable


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


class ArticleCommentType(BaseReplyType):
    pass


class ArticleCommentListType(graphene.ObjectType, interfaces=[PaginatorList]):
    article_comment_list = graphene.List(ArticleCommentType, )
