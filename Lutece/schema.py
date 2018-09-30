import graphene
from graphql_jwt import Verify
import user.schema as UserSchema
# import problem.schema as ProblemSchema
# import image.schema as ImageSchema
# import submission.schema as SubmissionSchema
# import article.schema as ArticleSchema
# import discussion.schema as DiscussionSchema


class Query( UserSchema.Query , graphene.ObjectType ):
    pass


class Mutations( UserSchema.Mutation , graphene.ObjectType):
    verify_token = Verify.Field()


schema = graphene.Schema( query = Query, mutation = Mutations )