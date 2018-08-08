import graphene
from .language import Language
from graphene.types.generic import GenericScalar
from graphql_jwt.decorators import login_required


class paginatorList(graphene.Interface):
    maxpage = graphene.Int(required=True)

class UploadImage( graphene.Mutation ):
    class Arguments:
        pass

    path = graphene.String()

    @login_required
    def mutate( self , info , * args , ** kwargs ):
        print( info )

class Query(object):
    all_language = graphene.Field(GenericScalar)

    def resolve_all_language(self, *args, **kwargs):
        return [x.value.attribute for x in Language]

class Mutation(graphene.AbstractType):
    UploadImage = UploadImage.Field()