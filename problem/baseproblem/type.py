import graphene
from graphene_django.types import DjangoObjectType
from problem.baseproblem.models import AbstractProblem
from utils.interface import PaginatorList

class AbstractProblemType( DjangoObjectType ):
    class Meta:
        model = AbstractProblem
        only_fields = ( 'title' , 'content' , 'resources' , 'constraints' , 'note' , 'slug' )
    
    pk = graphene.ID()

    def resolve_pk( self , info , * args , ** kwargs ):
        return self.pk

class AbstractProblemListType( graphene.ObjectType ):
    class Meta:
        interfaces = ( PaginatorList , )
    problem_list = graphene.List( AbstractProblemType )