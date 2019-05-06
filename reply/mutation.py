import graphene
from graphql import ResolveInfo, GraphQLError
from graphql_jwt.decorators import login_required

from reply.form import UpdateBaseReplyForm
from reply.models import BaseReply


class UpdateBaseReply(graphene.Mutation):
    class Arguments:
        pk = graphene.ID(required=True)
        content = graphene.String(required=True)

    state = graphene.Boolean()

    def mutate(self: None, info: ResolveInfo, **kwargs):
        update_article_comment = UpdateBaseReplyForm(kwargs)
        if update_article_comment.is_valid():
            values = update_article_comment.cleaned_data
            usr = info.context.user
            comment = BaseReply.objects.get(pk=values.get('pk'))
            if not usr.has_perm('reply.change_basereply') and usr != comment.author:
                raise PermissionError('Permission Denied.')
            comment.content = values.get('content')
            comment.save()
            return UpdateBaseReply(state=True)
        else:
            raise GraphQLError(update_article_comment.errors.as_json())


class CreateCommentReply(graphene.Mutation):
    class Arguments:
        parent = graphene.ID(required=True)
        content = graphene.String(required=True)

    state = graphene.Boolean()

    @login_required
    def mutate(self: None, info: ResolveInfo, **kwargs):
        create_comment_reply = CreateCommentReply(kwargs)
        if create_comment_reply.is_valid():
            values = create_comment_reply.cleaned_data
            usr = info.context.user
            parent = BaseReply.objects.get(pk=values.get('parent'))
            BaseReply.objects.create(
                content=values.get('content'),
                reply=parent,
                ancestor=parent.ancestor if parent.ancestor else parent,
                author=usr
            )
            return CreateCommentReply(state=True)
        else:
            raise GraphQLError(create_comment_reply.errors.as_json())


class Mutation(graphene.AbstractType):
    update_base_reply = UpdateBaseReply.Field()
    create_comment_reply = CreateCommentReply.Field()
