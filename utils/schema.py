import graphene
from .language import Language

class paginatorList( graphene.Interface ):
    maxpage = graphene.Int( required = True )



class Query( object ):
    pass
#    all_language = graphene.List( )