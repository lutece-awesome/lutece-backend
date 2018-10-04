import graphene
from problem.models import Problem
from problem.type import ProblemType, ProblemListType
from django.core.paginator import Paginator
from problem.constant import PER_PAGE_COUNT

class Query(object):
    problem = graphene.Field( ProblemType , slug = graphene.String() )
    problem_list = graphene.Field( ProblemListType , page = graphene.Int() , filter = graphene.String() )
    problem_search = graphene.Field( ProblemListType , filter = graphene.String() )

    def resolve_problem( self , info , * args , ** kwargs ):
        obj = Problem.objects.all()
        slug = kwargs.get( 'slug' )
        privileage = info.context.user.has_perm( 'problem.view' )
        if not privileage:
            obj = obj.filter( disable = False )
        return obj.get( slug = slug )

    def resolve_problem_list( self , info , * args , ** kwargs ):
        page = kwargs.get( 'page' )
        filter = kwargs.get( 'filter' )
        obj = Problem.objects.all()
        privileage = info.context.user.has_perm( 'problem.view' )
        if not privileage:
            obj = obj.filter( disable = False )
        if filter:
            obj = obj.filter( title__icontains = filter )
        paginator = Paginator( obj , PER_PAGE_COUNT )
        return ProblemListType( maxpage = paginator.num_pages, problem_list = paginator.get_page( page ) )
    
    def resolve_problem_search( self , info , * args , ** kwargs ):
        filter = kwargs.get('filter')
        problem_list = Problem.objects.all()
        if not info.context.user.has_perm('problem.view_all'):
            problem_list = problem_list.filter( disable = False )
        if filter:
            problem_list = problem_list.filter( title__icontains = filter )
        return ProblemListType( maxpage = 1 , problem_list = problem_list[:5] )