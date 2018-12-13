import graphene
from graphql import ResolveInfo
from graphql_jwt.decorators import permission_required

from article.form import UpdateHomeArticleForm, CreateHomeArticleForm
from article.models import HomeArticle
from utils.function import assign


class UpdateHomeArticle(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        slug = graphene.String(required=True)
        preview = graphene.String(required=True)
        content = graphene.String(required=True)
        disable = graphene.Boolean(required=True)

    state = graphene.Boolean()

    @permission_required('article.change_homearticle')
    def mutate(self: None, info: ResolveInfo, **kwargs):
        update_home_article_form = UpdateHomeArticleForm(kwargs)
        if update_home_article_form.is_valid():
            values = update_home_article_form.cleaned_data
            article = HomeArticle.objects.get(slug=values.get('slug'))
            assign(article, **values)
            article.save()
            return UpdateHomeArticle(state=True)
        else:
            raise RuntimeError(update_home_article_form.errors.as_json())


class CreateHomeArticle(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        preview = graphene.String(required=True)
        content = graphene.String(required=True)
        disable = graphene.Boolean(required=True)

    @permission_required('article.add_homearticle')
    def mutate(self: None, info: ResolveInfo, **kwargs):
        print(info)
        create_home_article_form = CreateHomeArticleForm(kwargs)
        if create_home_article_form.is_valid():
            values = create_home_article_form.cleaned_data
            article = HomeArticle(
                **values,
                author=info.context.user
            )
            article.save()
            return CreateHomeArticle(slug=article.slug)
        else:
            raise RuntimeError(create_home_article_form.errors.as_json())

    slug = graphene.String()


class Mutation(graphene.AbstractType):
    update_home_article = UpdateHomeArticle.Field()
    create_home_article = CreateHomeArticle.Field()
