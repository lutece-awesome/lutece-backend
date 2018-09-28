import graphene

class paginatorList(graphene.Interface):
    maxpage = graphene.Int( required = True )