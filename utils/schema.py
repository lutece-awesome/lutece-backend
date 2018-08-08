import graphene
from .language import Language
from graphene.types.generic import GenericScalar
from graphql_jwt.decorators import login_required
from graphene_file_upload import Upload


class paginatorList(graphene.Interface):
    maxpage = graphene.Int(required=True)

class UploadImage( graphene.Mutation ):
    class Arguments:
        file = Upload( required = True )

    path = graphene.String()

    @login_required
    def mutate( self , info , * args , ** kwargs ):
        file = info.context.FILES['0']
        return UploadImage( path = '666' )

class Query(object):
    all_language = graphene.Field(GenericScalar)

    def resolve_all_language(self, *args, **kwargs):
        return [x.value.attribute for x in Language]

class Mutation(graphene.AbstractType):
    UploadImage = UploadImage.Field()
