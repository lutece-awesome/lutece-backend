import graphene
from graphql_jwt.decorators import login_required

class UpdateAttachInfoMixin( graphene.Mutation ):
    class Arguments:
        school = graphene.String()
        company = graphene.String()
        location = graphene.String()
        about = graphene.String()
        gravatar = graphene.String()
        
    @login_required
    def mutate(self, info, ** kwargs):
        from user.attachinfo.form import AttachInfoForm
        attach_info_form = AttachInfoForm( ** kwargs )
        if attach_info_form.is_valid():
            values = attach_info_form.cleaned_data
            user = info.context.user
            for key , value in values.items():
                setattr( user , key , value )
            user.save()
            return UserInfoUpdate( state = True )
        else:
            raise RuntimeError( attach_info_form.errors.as_json() )