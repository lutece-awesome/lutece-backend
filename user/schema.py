import graphene
from graphene_django.types import DjangoObjectType
from .models import User
from annoying.functions import get_object_or_None


class UserType( DjangoObjectType ):
    class Meta:
        model = User
        only_fields = ( 'id' , 'display_name' , 'group' , 'school' , 'company' , 'location' , 'about' , 'tried' , 'solved' )

class UserLogout( graphene.Mutation ):

    state = graphene.Boolean()

    def mutate( self , info ):
        from graphql_jwt.shortcuts import get_token
        

class Query( object ):
    
    all_user = graphene.List( UserType )
    
    def resolve_all_user( self , info , ** kwargs ):
        return User.objects.all()

class Mutation( graphene.AbstractType ):
    pass
