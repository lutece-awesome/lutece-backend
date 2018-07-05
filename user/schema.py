import graphene
from graphene_django.types import DjangoObjectType
from .models import User
from annoying.functions import get_object_or_None


class UserType( DjangoObjectType ):
    class Meta:
        model = User
        only_fields = ( 'id' , 'display_name' )


class UserLogin( graphene.Mutation ):
    class Arguments:
        username = graphene.String( required = True )
        password = graphene.String( required = True )
    
    state = graphene.Boolean()
    msg = graphene.String()

    def mutate( self , info , username , password ):
        login_user = get_object_or_None( User , username = username )
        from django.contrib.auth import login
        if not login_user:
            return UserLogin( state = False , msg = 'No such user' )
        elif login_user.check_password( password ):
            login( info.context , login_user )
            return UserLogin( state = True )
        else:
            return UserLogin( state = False , msg = 'Wrong password' )

class Query( object ):

    all_user = graphene.List( UserType )
    user_authed = graphene.Boolean()
    
    def resolve_all_user( self , info , ** kwargs ):
        return User.objects.all()

    def resolve_user_authed( self , info ):
        return info.context.user.is_authenticated
        
class Mutation( graphene.AbstractType ):
    UserLogin = UserLogin.Field()
