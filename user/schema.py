import graphene
from graphene_django.types import DjangoObjectType
from .models import User


class UserType( DjangoObjectType ):
    class Meta:
        model = User
        only_fields = ( 'id' , 'display_name'  )

class Query( object ):

    all_user = graphene.List( UserType )
    
    def resolve_all_user( self , info , ** kwargs ):
        return User.objects.all()
