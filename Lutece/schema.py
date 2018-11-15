import graphene
from graphql_jwt import Verify

from problem.mutation import Mutation as ProblemMutationSchema
from problem.query import Query as ProblemQuerySchema
from submission.mutation import Mutation as SubmissionMutationSchema
from submission.query import Query as SubmissionQuerySchema
from user.mutation import Mutation as UserMutationSchema
from user.query import Query as UserQuerySchema


# import problem.schema as ProblemSchema
# import image.schema as ImageSchema
# import submission.schema as SubmissionSchema
# import article.schema as ArticleSchema
# import discussion.schema as DiscussionSchema


class Query(UserQuerySchema, ProblemQuerySchema, SubmissionQuerySchema, graphene.ObjectType):
    pass


class Mutations(UserMutationSchema, ProblemMutationSchema, SubmissionMutationSchema, graphene.ObjectType):
    verify_token = Verify.Field()


schema = graphene.Schema(query=Query, mutation=Mutations)
