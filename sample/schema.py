import graphene


class AbstractSampleType( DjangoObjectType ):
    pk = graphene.ID()
    input_content = graphene.String()
    output_content = graphene.String()

    def resolve_pk( self , info , * args , ** kwargs ):
        return self.pk

    def resolve_input_content( self , info , * args , ** kwargs ):
        return self.input_content
    
    def resolve_output_content( self , info , * args , ** kwargs ):
        return self.output_content
