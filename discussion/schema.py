import graphene
from graphene_django.types import DjangoObjectType
from annoying.functions import get_object_or_None
from .models import Discussion as AbstractDiscussion
from .models import DiscussionVote
from user.schema import UserType
from graphene.types.generic import GenericScalar
from graphql_jwt.decorators import login_required


class ReplyType( DjangoObjectType ):
    class Meta:
        model = AbstractDiscussion
        only_fields = ( 'vote' , 'submit_time' , 'visibility' )
    
    pk = graphene.ID()
    user = graphene.Field( UserType )
    content = graphene.String()
    attitude = graphene.String()

    def resolve_pk( self , info , * args , ** kwargs ):
        return self.pk

    def resolve_content( self , info , * args , ** kwargs ):
        privileage = info.context.user.has_perm( 'discussion.view_all' )
        if not self.visibility and not privileage:
            return ''
        return self.content

    def resolve_user( self , info , * args , ** kwargs ):
        return self.user

    def resolve_attitude( self , info , * args , ** kwargs ):
        if info.context.user.is_authenticated:
            s = get_object_or_None( DiscussionVote , discussion = self , user = info.context.user )
        else:
            s = None
        return s.vote if s else DiscussionVote.neutral


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

class Query(object):
    pass

class Mutation(graphene.AbstractType):
    UpdateDiscussionVote = UpdateDiscussionVote.Field()