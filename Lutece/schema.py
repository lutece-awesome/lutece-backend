import graphene
import user.schema as UserSchema

class Query( UserSchema.Query , graphene.ObjectType ):
    pass

schema = graphene.Schema(query=Query)
