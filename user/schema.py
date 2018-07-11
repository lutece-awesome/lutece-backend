import graphene
from graphene_django.types import DjangoObjectType
from .models import User
from annoying.functions import get_object_or_None
from graphql_jwt.shortcuts import get_token
from .group import Group

class UserType( DjangoObjectType ):
    class Meta:
        model = User
        only_fields = ( 'id' , 'display_name' , 'group' , 'school' , 'company' , 'location' , 'about' , 'tried' , 'solved' )

class Register( graphene.Mutation  ):
    class Arguments:
        username = graphene.String( required = True )
        password = graphene.String( required = True )
        email = graphene.String( required = True )
        displayname = graphene.String( required = True )
        school = graphene.String()
        company = graphene.String()
        location = graphene.String()

    token = graphene.String()

    def mutate( self , info , ** kwargs ):
        from .form import UserSignupForm
        SignupForm = UserSignupForm( kwargs )
        if SignupForm.is_valid():
            values = SignupForm.cleaned_data
            new_user = User(
                username = values['username'],
                email = values['email'],
                display_name = values['displayname'],
                is_staff = False,
                is_superuser = False,)
            new_user.set_password( values['password'] )
            new_user.save()
            new_user.set_group( Group.NORMAL_USER )
            return Register( token = get_token( new_user ) )
        else:
            raise RuntimeError( SignupForm.errors.as_json() )


class Query( object ):
    
    all_user = graphene.List( UserType )
    
    def resolve_all_user( self , info , ** kwargs ):
        return User.objects.all()

class Mutation( graphene.AbstractType ):
    Register = Register.Field()
