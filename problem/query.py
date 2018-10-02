import graphene
from problem.models import Problem
from problem.type import ProblemType, ProblemListType
from django.core.paginator import Paginator
from problem.constant import PER_PAGE_COUNT

class Query(object):
    problem = graphene.Field( ProblemType , slug = graphene.String() )
    problem_list = graphene.Field( ProblemListType , page = graphene.Int() , filter = graphene.String() )

    def resolve_problem( self , info , * args , ** kwargs ):
        obj = Problem.objects.all()
        slug = kwargs.get( 'slug' )
        privileage = info.context.user.has_perm( 'Problem.view' )
        if not privileage:
            obj = obj.filter( disable = False )
        return obj.get( slug = slug )

    def resolve_problem_list( self , info , * args , ** kwargs ):
        page = kwargs.get( 'page' )
        filter = kwargs.get( 'filter' )
        obj = Problem.objects.all()
        privileage = info.context.user.has_perm( 'Problem.view' )
        if not privileage:
            obj = obj.filter( disable = False )
        if filter:
            obj = obj.filter( title__icontains = filter )
        paginator = Paginator( obj , PER_PAGE_COUNT )
        return ProblemListType( maxpage = paginator.num_pages, problem_list = paginator.get_page( page ) )