import graphene
from image.form import UploadImageForm
from graphene_file_upload.scalars import Upload
from graphql_jwt.decorators import login_required


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
        image_form = UploadImageForm( request.POST , request.FILES )
        if image_form.is_valid():
            values = image_form.cleaned_data
            s = UploadFile(
                image = values['image'],
                user = request.user
            )
            s.save()
            return UploadImage( path = s.image.url )
        else:
            raise RuntimeError( image_form.errors.as_json() )

class Mutation(graphene.AbstractType):
    uploadImage = UploadImage.Field()
