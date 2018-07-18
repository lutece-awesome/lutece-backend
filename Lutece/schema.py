import graphene
import graphql_jwt
import user.schema as UserSchema
import problem.schema as ProblemSchema
import utils.schema as UtilsSchema

class Query( UserSchema.Query , ProblemSchema.Query , UtilsSchema.Query , graphene.ObjectType ):
    pass

class Mutations( UserSchema.Mutation , ProblemSchema.Mutation , UtilsSchema.Mutation , graphene.ObjectType):
    verify_token = graphql_jwt.Verify.Field()

schema = graphene.Schema( query = Query , mutation = Mutations )
