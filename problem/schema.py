import graphene
from graphene_django.types import DjangoObjectType
from .models import Problem
from utils.schema import paginatorList

class ProblemType( DjangoObjectType ):
    class Meta:
        model = Problem
        only_fields = ( 'problem_id' , 'title' , 'content' , 'standardInput' , 'standardOutput' , 'constraints' , 'resource' , 'note' , 'time_limit' , 'memory_limit' , 'submit' , 'accept' , 'slug' )

class ProblemListType( graphene.ObjectType ):
    class Meta:
        interfaces = ( paginatorList , )
    problemList = graphene.List( ProblemType )

class Query( object ):
    problem = graphene.Field( ProblemType , pk = graphene.ID() )
    problemList = graphene.Field( ProblemListType , page = graphene.Int() )
    problemsearch = graphene.List( ProblemType , title = graphene.String() )

    def resolve_problem( self , info , pk ):
        return Problem.objects.get( pk = pk )

    def resolve_problemList( self , info , page ):
        from django.core.paginator import Paginator
        from Lutece.config import PER_PAGE_COUNT
        problem_list = Problem.objects.all()
        if not info.context.user.has_perm( 'problem.view_all' ):
            problem_list = problem_list.filter( visible = True )
        paginator = Paginator( problem_list , PER_PAGE_COUNT )
        return ProblemListType( maxpage = paginator.num_pages , problemList = paginator.get_page( page ) )

    def resolve_problemsearch( self , info , title ):
        _all = Problem.objects.all()
        if not info.context.user.has_perm( 'problem.view_all' ):
            _all = _all.filter( visible = True )
        return list(_all.filter( title__contains = title )[:5])

class Mutation( graphene.AbstractType ):
    pass