import graphene
from problem.baseproblem.models import AbstractProblem
from problem.baseproblem.type import AbstractProblemType, AbstractProblemListType
from django.core.paginator import Paginator
from problem.constant import PER_PAGE_COUNT

class Query(object):
    problem = graphene.Field( AbstractProblemType , slug = graphene.String() )
    problem_list = graphene.Field( AbstractProblemListType , page = graphene.Int() , filter = graphene.String() )

    def resolve_problem( self , info , * args , ** kwargs ):
        obj = AbstractProblem.objects.all()
        slug = kwargs.get( 'slug' )
        privileage = info.context.user.has_perm( 'AbstractProblem.view' )
        if not privileage:
            obj = obj.filter( disable = False )
        return obj.get( slug = slug )
    
    def resolve_problem_list( self , info , * args , ** kwargs ):
        page = kwargs.get( 'page' )
        filter = kwargs.get( 'filter' )
        obj = AbstractProblem.objects.all()
        privileage = info.context.user.has_perm( 'AbstractProblem.view' )
        if not privileage:
            obj = obj.filter( disable = False )
        if filter:
            obj = obj.filter( title__icontains = filter )
        paginator = Paginator( obj , PER_PAGE_COUNT )
        return AbstractProblemListType( maxpage = paginator.num_pages, problem_list = paginator.get_page( page ) )