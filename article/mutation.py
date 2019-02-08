import graphene
from graphql import ResolveInfo, GraphQLError
from graphql_jwt.decorators import permission_required, login_required

from article.form import UpdateHomeArticleForm, CreateHomeArticleForm, CreateUserArticleForm, UpdateUserArticleForm, \
    UpdateArticleRecordForm
from article.models import HomeArticle, UserArticle, ArticleRecord, Article
from utils.function import assign


class UpdateHomeArticle(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        slug = graphene.String(required=True)
        preview = graphene.String(required=True)
        content = graphene.String(required=True)
        disable = graphene.Boolean(required=True)

    slug = graphene.String()

    @permission_required('article.change_homearticle')
    def mutate(self: None, info: ResolveInfo, **kwargs):
        update_home_article_form = UpdateHomeArticleForm(kwargs)
        if update_home_article_form.is_valid():
            values = update_home_article_form.cleaned_data
            article = HomeArticle.objects.get(slug=values.get('slug'))
            assign(article, **values)
            article.save()
            return UpdateHomeArticle(slug=article.slug)
        else:
            raise GraphQLError(update_home_article_form.errors.as_json())


class CreateHomeArticle(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        preview = graphene.String(required=True)
        content = graphene.String(required=True)

    slug = graphene.String()

    @permission_required('article.add_homearticle')
    def mutate(self: None, info: ResolveInfo, **kwargs):
        create_home_article_form = CreateHomeArticleForm(kwargs)
        if create_home_article_form.is_valid():
            values = create_home_article_form.cleaned_data
            article = HomeArticle.objects.create(
                **values,
                author=info.context.user,
                record=ArticleRecord.objects.create()
            )
            return CreateHomeArticle(slug=article.slug)
        else:
            raise RuntimeError(create_home_article_form.errors.as_json())


class UpdateUserArticle(graphene.Mutation):
    class Arguments:
        pk = graphene.ID(required=True)
        title = graphene.String(required=True)
        content = graphene.String(required=True)

    state = graphene.Boolean()

    def mutate(self: None, info: ResolveInfo, **kwargs):
        update_user_article_form = UpdateUserArticleForm(kwargs)
        if update_user_article_form.is_valid():
            values = update_user_article_form.cleaned_data
            article = UserArticle.objects.get(pk=values.get('pk'))
            if article.author != info.context.user and not info.context.user.has_perm('article.change_userarticle'):
                raise PermissionError('Permission Denied')
            article.title = values.get('title')
            article.content = values.get('content')
            article.save()
            return UpdateUserArticle(state=True)
        else:
            raise RuntimeError(update_user_article_form.errors.as_json())


class CreateUserArticle(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        content = graphene.String(required=True)

    pk = graphene.ID()

    @login_required
    def mutate(self: None, info: ResolveInfo, **kwargs):
        create_user_article_form = CreateUserArticleForm(kwargs)
        if create_user_article_form.is_valid():
            values = create_user_article_form.cleaned_data
            article = UserArticle.objects.create(
                **values,
                author=info.context.user,
                record=ArticleRecord.objects.create()
            )
            return CreateUserArticle(pk=article.pk)
        else:
            raise RuntimeError(create_user_article_form.errors.as_json())


class UpdateArticleRecord(graphene.Mutation):
    class Arguments:
        pk = graphene.ID(required=True)

    state = graphene.Boolean()

    def mutate(self: None, info: ResolveInfo, **kwargs):
        update_article_record = UpdateArticleRecordForm(kwargs)
        if update_article_record.is_valid():
            values = update_article_record.cleaned_data
            article = Article.objects.get(pk=values.get('pk'))
            article.record.increase()
            article.record.save()
            return UpdateArticleRecord(state=True)
        else:
            raise RuntimeError(update_article_record.errors.as_json())


class Mutation(graphene.AbstractType):
    update_home_article = UpdateHomeArticle.Field()
    create_home_article = CreateHomeArticle.Field()
    update_user_article = UpdateUserArticle.Field()
    create_user_article = CreateUserArticle.Field()
    update_article_record = UpdateArticleRecord.Field()
