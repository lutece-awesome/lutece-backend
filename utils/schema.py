import graphene
from .language import Language
from graphene.types.generic import GenericScalar


class paginatorList(graphene.Interface):
    maxpage = graphene.Int(required=True)


class Query(object):
    all_language = graphene.Field(GenericScalar)

    def resolve_all_language(self, *args, **kwargs):
        return [x.value.attribute for x in Language]


class Mutation(graphene.AbstractType):
    pass
