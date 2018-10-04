import graphene
from graphene_django.types import DjangoObjectType
from problem.limitation.type import AbstractLimiationType
from problem.models import Problem, ProblemSample
from utils.interface import PaginatorList

class ProblemSampleType( DjangoObjectType ):
    class Meta:
        model = ProblemSample
        only_fields = ( "input_content" , 'output_content' )

class ProblemSampleListType( graphene.ObjectType ):
    sample_list = graphene.List( ProblemSampleType , )

class ProblemType( DjangoObjectType ):
    class Meta:
        model = Problem
        only_fields = ( 'title' , 'content' , 'resources' , 'constraints' , 'note' , 'slug' , 'standard_input' , 'standard_output' , 'submit' , 'accept' )

    pk = graphene.ID()
    limitation = graphene.Field( AbstractLimiationType )
    samples = graphene.Field( ProblemSampleListType )

    def resolve_pk( self , info , * args , ** kwargs ):
        return self.pk

    def resolve_limitation( self , info , * args , ** kwargs ):
        return self.limitation
    
    def resolve_samples( self , info , * args , ** kwargs ):
        result = ProblemSample.objects.filter( problem = self )
        return ProblemSampleListType( sample_list = result )

class ProblemListType( graphene.ObjectType ):
    class Meta:
        interfaces = ( PaginatorList , )
    problem_list = graphene.List( ProblemType , )