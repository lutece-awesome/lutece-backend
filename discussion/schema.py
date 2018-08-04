import graphene
from graphene_django.types import DjangoObjectType
from annoying.functions import get_object_or_None
from .models import Discussion
from user.schema import UserType

class DiscussionType( DjangoObjectType ):
    class Meta:
        model = Discussion
        only_fields = ( 'discussion_id' , 'reply' , 'submit_time' , 'vote' )

    user = graphene.Field( UserType )
    content = graphene.String()

    def resolve_user( self , info , * args , ** kwargs ):
        return self.user

    def resolve_content( self , info , * args , ** kwargs ):
        privileage = info.context.user.has_perm( 'discussion.view_all' )
        if not self.visibility and not privileage:
            return ''
        return self.content
        

class Query(object):
    pass


class Mutation(graphene.AbstractType):
    pass