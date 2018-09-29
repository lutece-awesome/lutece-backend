import graphene
from graphene_django.types import DjangoObjectType
from annoying.functions import get_object_or_None
from reply.models import AbstractReply, AbstractReplyVote, Attitude
from user.schema import UserType
from graphene.types.generic import GenericScalar
from graphql_jwt.decorators import login_required


class AbstractReplyType( DjangoObjectType ):    
    pk = graphene.ID()
    content = graphene.String()
    user = graphene.Field( UserType )
    vote = graphene.Int()
    self_attitude = graphene.String()

    def resolve_pk( self , info , * args , ** kwargs ):
        return self.pk

    def resolve_content( self , info , * args , ** kwargs ):
        privileage = info.context.user.has_perm( 'AbstractReply.view' )
        if self.disable and not privileage:
            return ''
        return self.content

    def resolve_user( self , info , * args , ** kwargs ):
        return self.user

    def resolve_vote( self , info , * args , ** kwargs ):
        return AbstractReplyVote.objects.filter( reply = self , attitude = Attitude.agree ).count() - AbstractReply.objects.filter( reply = self , attitude = Attitude.disagree ).count()

    def resolve_self_attitude( self , info , * args , ** kwargs ):
        user = info.context.user
        if not user.is_authenticated:
            return Attitude.neutral
        vote = get_object_or_None( AbstractReplyVote , reply = self , record_user = user )
        if vote is None:
            return Attitude.neutral
        return vote.attitude


class DiscussionType( graphene.AbstractType ):
    pk = graphene.ID()
    user = graphene.Field( UserType )
    content = graphene.String()
    vote = graphene.Int()
    submit_time = graphene.DateTime()
    reply = graphene.List( ReplyType )
    attitude = graphene.String()
    visibility = graphene.Boolean()

    def resolve_pk( self , info , * args , ** kwargs ):
        return self.pk

    def resolve_user( self , info , * args , ** kwargs ):
        return self.user

    def resolve_content( self , info , * args , ** kwargs ):
        privileage = info.context.user.has_perm( 'discussion.view_all' )
        if not self.visibility and not privileage:
            return ''
        return self.content

    def resolve_vote( self , info , * args , ** kwargs ):
        return self.vote

    def resolve_submit_time( self , info , * args , ** kwargs ):
        return self.submit_time

    def resolve_reply( self , info , * args , ** kwargs ):
        return list( AbstractDiscussion.objects.filter( ancestor = self.pk ) )

    def resolve_attitude( self , info , * args , ** kwargs ):
        if info.context.user.is_authenticated:
            s = get_object_or_None( DiscussionVote , discussion = self , user = info.context.user )
        else:
            s = None
        return s.vote if s else DiscussionVote.neutral
    
    def resolve_visibility( self , info , * args , ** kwargs ):
        return self.visibility

class UpdateDiscussionVote(graphene.Mutation):

    class Arguments:
        attitude = graphene.Boolean( required = True )
        pk = graphene.ID( required = True )

    result = graphene.String()
    vote = graphene.Int()

    @login_required
    def mutate(self, info , pk , attitude ):
        from json import loads
        i = AbstractDiscussion.objects.get( pk = pk )
        s , created = DiscussionVote.objects.get_or_create(
            user = info.context.user,
            discussion = i
        )
        ret = DiscussionVote.agree if attitude else DiscussionVote.disagree            
        s.vote = ret if ret != s.vote or created else DiscussionVote.neutral
        s.save()
        i.refresh_vote()
        return UpdateDiscussionVote( result = s.vote , vote = i.vote )

class ReplyDiscussion(graphene.Mutation):
    class Arguments:
        parent = graphene.ID()
        content = graphene.String()
    
    state = graphene.Boolean()
    
    @login_required
    def mutate( self , info , * args , ** kwargs ):
        from .form import ReplyDiscussionForm
        replyDiscussionForm = ReplyDiscussionForm( ** kwargs )
        if replyDiscussionForm.is_valid():
            values = replyDiscussionForm.cleaned_data
            reply = AbstractDiscussion.objects.get( pk = values['parent'] )
            AbstractDiscussion(
                user = info.context.user,
                content = values['content'],
                reply = reply,
                ancestor = reply.ancestor if reply.ancestor else reply,
            ).save()
            return ReplyDiscussion( state = True )
        else:
            raise RuntimeError( replyDiscussionForm.errors.as_json() )

class Query(object):
    pass

class Mutation(graphene.AbstractType):
    UpdateDiscussionVote = UpdateDiscussionVote.Field()
    ReplyDiscussion = ReplyDiscussion.Field()