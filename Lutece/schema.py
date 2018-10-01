import graphene
from graphql_jwt import Verify
from user.query import Query as UserQuerySchema
from user.mutation import Mutation as UserMutationSchema
from problem.query import Query as ProblemQuerySchema
from problem.mutation import Mutation as ProblemMutationSchema
# import problem.schema as ProblemSchema
# import image.schema as ImageSchema
# import submission.schema as SubmissionSchema
# import article.schema as ArticleSchema
# import discussion.schema as DiscussionSchema


class Query( UserQuerySchema , ProblemQuerySchema , graphene.ObjectType ):
    pass


class Mutations( UserMutationSchema , ProblemMutationSchema , graphene.ObjectType):
    verify_token = Verify.Field()


schema = graphene.Schema( query = Query, mutation = Mutations )