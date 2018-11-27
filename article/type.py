import graphene
from graphql import ResolveInfo

from user.type import UserType


class ArticleType(graphene.ObjectType):
    pk = graphene.ID()
    title = graphene.String()
    author = graphene.Field(UserType)
    content = graphene.String()
    create_time = graphene.DateTime()
    last_update_time = graphene.DateTime()

    def resolve_pk(self, info: ResolveInfo):
        return self.pk

    def resolve_title(self, info: ResolveInfo):
        return self.title

    def resolve_author(self, info: ResolveInfo):
        return self.author

    def resolve_content(self, info: ResolveInfo):
        return self.content

    def resolve_create_time(self, info: ResolveInfo):
        return self.create_time

    def resolve_last_update_time(self, info: ResolveInfo):
        return self.last_update_time


class HomeArticleType(ArticleType):
    preview = graphene.String()

    def resolve_preview(self, info: ResolveInfo):
        return self.preview
