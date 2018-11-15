import graphene


class PaginatorList(graphene.Interface):
    maxpage = graphene.Int(required=True)
