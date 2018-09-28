import graphene
import graphql_jwt
import user.schema as UserSchema
import problem.schema as ProblemSchema
import image.schema as ImageSchema
import submission.schema as SubmissionSchema
import article.schema as ArticleSchema
import discussion.schema as DiscussionSchema


class Query(UserSchema.Query, ProblemSchema.Query, SubmissionSchema.Query, ArticleSchema.Query , graphene.ObjectType ):
    pass


class Mutations(UserSchema.Mutation, ProblemSchema.Mutation, ImageSchema.Mutation, SubmissionSchema.Mutation, ArticleSchema.Mutation , DiscussionSchema.Mutation , graphene.ObjectType):
    verify_token = graphql_jwt.Verify.Field()


schema = graphene.Schema( query = Query, mutation = Mutations )
