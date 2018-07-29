import graphene
from graphene_django.types import DjangoObjectType
from annoying.functions import get_object_or_None
from .models import Blog, BlogDiscussion, BlogVoteUser
from user.schema import UserType
from user.models import User
from graphql_jwt.decorators import login_required

class BlogType( DjangoObjectType ):
    class Meta:
        model = Blog
        only_fields = ( 'id' , 'title' , 'content' , 'create_time' , 'slug' )
    
    user = graphene.Field( UserType )

    def resolve_user( self , info , * args , ** kwargs ):
        return self.user
    


class CreateBlog( graphene.Mutation ):
    class Arguments:
        title = graphene.String( required = True )
        content = graphene.String( required = True )

    @login_required
    def mutate( self , info , * args , ** kwargs ):
        
        pass


class Query(object):
    blog = graphene.Field( BlogType , slug = graphene.String() )

    def resolve_blog( self , info , slug ):
        return Blog.objects.get( slug = slug )

class Mutation(graphene.AbstractType):
    pass
