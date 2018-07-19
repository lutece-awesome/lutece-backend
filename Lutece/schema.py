import graphene
import graphql_jwt
import user.schema as UserSchema
import problem.schema as ProblemSchema
import utils.schema as UtilsSchema
import submission.schema as SubmissionSchema

class Query( UserSchema.Query , ProblemSchema.Query , UtilsSchema.Query , SubmissionSchema.Query , graphene.ObjectType ):
    pass

class Mutations( UserSchema.Mutation , ProblemSchema.Mutation , UtilsSchema.Mutation , SubmissionSchema.Mutation , graphene.ObjectType):
    verify_token = graphql_jwt.Verify.Field()

schema = graphene.Schema( query = Query , mutation = Mutations )
