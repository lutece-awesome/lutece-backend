import graphene
from graphene_django.types import DjangoObjectType
from annoying.functions import get_object_or_None
from .models import Discussion as AbstractDiscussion
from .models import DiscussionVote
from user.schema import UserType
from graphene.types.generic import GenericScalar


class ReplyType( DjangoObjectType ):
    class Meta:
        model = AbstractDiscussion
        only_fields = ( 'vote' , 'submit_time' , 'visibility' )

    user = graphene.Field( UserType )
    content = graphene.String()
    has_voted = graphene.Boolean()

    def resolve_content( self , info , * args , ** kwargs ):
        privileage = info.context.user.has_perm( 'discussion.view_all' )
        if not self.visibility and not privileage:
            return ''
        return self.content

    def resolve_user( self , info , * args , ** kwargs ):
        return self.user

    def resolve_has_voted( self , info , * args , ** kwargs ):
        s = get_object_or_None( DiscussionVote , discussion = self )
        return s.vote if s else None


class DiscussionType( graphene.AbstractType ):
    pk = graphene.ID()
    user = graphene.Field( UserType )
    content = graphene.String()
    vote = graphene.Int()
    submit_time = graphene.DateTime()
    reply = graphene.List( ReplyType )
    has_voted = graphene.Boolean()
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
        return list( AbstractDiscussion.objects.filter( reply = self.pk ) )

    def resolve_has_voted( self , info , * args , ** kwargs ):
        s = get_object_or_None( DiscussionVote , discussion = self )
        return s.vote if s else None
    
    def resolve_visibility( self , info , * args , ** kwargs ):
        return self.visibility

class Query(object):
    pass

class Mutation(graphene.AbstractType):
    pass