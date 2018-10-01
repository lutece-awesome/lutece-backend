import graphene
from graphene_django.types import DjangoObjectType
from problem.limitation.models import Limitation

class LimiationType( DjangoObjectType ):
    class Meta:
        model = Limitation
        only_fields = ( "time_limit" , "memory_limit" , "output_limit" , "cpu_limit" )

    pk = graphene.ID()
    
    def resolve_pk( self , info , * args , ** kwargs ):
        return self.pk