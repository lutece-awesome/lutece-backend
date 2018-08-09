import graphene
from .language import Language
from graphene.types.generic import GenericScalar
from graphql_jwt.decorators import login_required
from graphene_file_upload import Upload
from .form import UploadImageForm
from .models import UploadFile

class paginatorList(graphene.Interface):
    maxpage = graphene.Int(required=True)

class UploadImage( graphene.Mutation ):
    class Arguments:
        file = Upload( required = True )

    path = graphene.String()

    @login_required
    def mutate( self , info , * args , ** kwargs ):
        request = info.context
        image = request.FILES['0']
        request.FILES.pop( '0' )
        request.FILES[ 'image' ] = image
        uploadImageForm = UploadImageForm( info.context.POST  , info.context.FILES )
        if uploadImageForm.is_valid():
            values = uploadImageForm.cleaned_data
            s = UploadFile(
                image = values['image'],
                user = info.context.user
            )
            s.save()
            return UploadImage( path = s.image.url )
        else:
            raise RuntimeError( uploadImageForm.errors.as_json() )

class Query(object):
    all_language = graphene.Field(GenericScalar)

    def resolve_all_language(self, *args, **kwargs):
        return [x.value.attribute for x in Language]

class Mutation(graphene.AbstractType):
    UploadImage = UploadImage.Field()
