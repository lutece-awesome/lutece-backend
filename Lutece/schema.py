import graphene
import graphql_jwt
import user.schema as UserSchema
import problem.schema as ProblemSchema
import utils.schema as UtilsSchema
import submission.schema as SubmissionSchema
import blog.schema as BlogSchema
import discussion.schema as DiscussionSchema


class Query(UserSchema.Query, ProblemSchema.Query, UtilsSchema.Query, SubmissionSchema.Query, BlogSchema.Query , graphene.ObjectType ):
    pass


class Mutations(UserSchema.Mutation, ProblemSchema.Mutation, UtilsSchema.Mutation, SubmissionSchema.Mutation, BlogSchema.Mutation , DiscussionSchema.Mutation , graphene.ObjectType):
    verify_token = graphql_jwt.Verify.Field()


schema = graphene.Schema(query=Query, mutation=Mutations)
