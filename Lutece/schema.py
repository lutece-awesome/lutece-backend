import graphene
from graphql_jwt import Verify

from article.mutation import Mutation as ArticleMutationSchema
from article.query import Query as ArticleQuerySchema
from problem.mutation import Mutation as ProblemMutationSchema
from problem.query import Query as ProblemQuerySchema
from reply.mutation import Mutation as ReplyMutationSchema
from submission.mutation import Mutation as SubmissionMutationSchema
from submission.query import Query as SubmissionQuerySchema
from user.mutation import Mutation as UserMutationSchema
from user.query import Query as UserQuerySchema


class Query(UserQuerySchema, ProblemQuerySchema, SubmissionQuerySchema, ArticleQuerySchema, graphene.ObjectType):
    pass


class Mutations(UserMutationSchema, ProblemMutationSchema, SubmissionMutationSchema, ArticleMutationSchema,
                ReplyMutationSchema,
                graphene.ObjectType):
    verify_token = Verify.Field()


schema = graphene.Schema(query=Query, mutation=Mutations)
