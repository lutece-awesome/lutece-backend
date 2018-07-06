import graphene
from graphene_django.types import DjangoObjectType
from .models import Problem

class ProblemType( DjangoObjectType ):
    class Meta:
        model = Problem
        only_fields = ( 'problem_id' , 'title' , 'content' , 'standardInput' , 'standardOutput' , 'constraints' , 'resource' , 'note' , 'time_limit' , 'memory_limit' , 'submit' , 'accept' )


class Query( object ):
    problem = graphene.Field( ProblemType , pk = graphene.ID() )
    problemList = graphene.List( ProblemType , page = graphene.Int() )

    def resolve_problem( self , info , pk ):
        return Problem.objects.get( pk = pk )

    def resolve_problemList( self , info , page ):
        print( info.context.user.is_authenticated )
        return Problem.objects.all()

class Mutation( graphene.AbstractType ):
    pass