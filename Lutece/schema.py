import graphene
import graphql_jwt
import user.schema as UserSchema

class Query( UserSchema.Query , graphene.ObjectType ):
    pass

class Mutations( UserSchema.Mutation , graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()

schema = graphene.Schema( query = Query , mutation=Mutations )
