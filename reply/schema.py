import graphene
from annoying.functions import get_object_or_None
from graphene_django.types import DjangoObjectType
from graphql_jwt.decorators import login_required
from user.schema import UserType

from reply.models import AbstractReply, AbstractReplyVote, Attitude


class AbstractReplyType(DjangoObjectType):
    pk = graphene.ID()
    content = graphene.String()
    user = graphene.Field(UserType)
    vote = graphene.Int()
    self_attitude = graphene.String()
    discussion = graphene.List(AbstractReplyType)
    disable = graphene.Boolean()

    def resolve_pk(self, info, *args, **kwargs):
        return self.pk

    def resolve_content(self, info, *args, **kwargs):
        privileage = info.context.user.has_perm('AbstractReply.view')
        if self.disable and not privileage:
            return ''
        return self.content

    def resolve_user(self, info, *args, **kwargs):
        return self.user

    def resolve_vote(self, info, *args, **kwargs):
        return AbstractReplyVote.objects.filter(reply=self,
                                                attitude=Attitude.agree).count() - AbstractReply.objects.filter(
            reply=self, attitude=Attitude.disagree).count()

    def resolve_self_attitude(self, info, *args, **kwargs):
        user = info.context.user
        if not user.is_authenticated:
            return Attitude.neutral
        vote = get_object_or_None(AbstractReplyVote, reply=self, record_user=user)
        if vote is None:
            return Attitude.neutral
        return vote.attitude

    def resolve_discussion(self, info, *args, **kwargs):
        return list(AbstractReply.objects.filter(ancestor=self.pk))

    def resolve_disable(self, info, *args, **kwargs):
        return self.disable


class UpdateAbstractReplyVote(graphene.Mutation):
    class Arguments:
        attitude = graphene.Boolean(required=True)
        reply_pk = graphene.ID(required=True)

    result = graphene.String()

    @login_required
    def mutate(self, info, reply_pk, attitude):
        reply = AbstractReply.objects.get(pk=reply_pk)
        node, created = AbstractReplyVote.objects.get_or_create(
            user=info.context.user,
            discussion=i
        )
        attitude = Attitude.agree if attitude else Attitude.disagree
        node.vote = attitude if created or attitude != node.vote else Attitude.neutral
        node.save()
        return UpdateReplyVote(result=attitude)


class CreateAbstractReply(graphene.Mutation):
    class Arguments:
        parent = graphene.ID()
        content = graphene.String()

    state = graphene.Boolean()

    @login_required
    def mutate(self, info, *args, **kwargs):
        from reply.form import AbstractReplyForm
        reply_form = AbstractReplyForm(**kwargs)
        if reply_form.is_valid():
            values = reply_form.cleaned_data
            parent = AbstractReply.objects.get(pk=values['parent'])
            AbstractReply(
                user=info.context.user,
                content=values['content'],
                parent=parent,
                ancestor=parent.ancestor if parent.ancestor else parent,
            ).save()
            return CreateAbstractReply(state=True)
        else:
            raise RuntimeError(reply_form.errors.as_json())
