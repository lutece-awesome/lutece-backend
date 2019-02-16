import graphene


class PaginatorList(graphene.Interface):
    max_page = graphene.Int(required=True)
