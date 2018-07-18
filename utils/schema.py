import graphene
from .language import Language

class paginatorList( graphene.Interface ):
    maxpage = graphene.Int( required = True )

class Query( object ):
    all_language = graphene.Field( graphene.JSONString )

    def resolve_all_language( self , * args , ** kwargs ):
        return [ x.value.attribute for x in Language ]

class Mutation( graphene.AbstractType ):
    pass
