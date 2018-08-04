import graphene
from graphene_django.types import DjangoObjectType
from annoying.functions import get_object_or_None
from .models import Discussion
from user.schema import UserType

class DiscussionType( graphene.AbstractType ):
    pk = graphene.ID()
    user = graphene.Field( UserType )
    content = graphene.String()
    vote = graphene.Int()
    submit_time = graphene.DateTime()
    reply = graphene.ID()

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

    # For security reason, recurse are not allowed here
    def resolve_reply( self , info , * args , ** kwargs ):
        return self.reply.pk if self.reply else None

class Query(object):
    pass

class Mutation(graphene.AbstractType):
    pass