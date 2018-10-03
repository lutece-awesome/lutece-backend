import graphene
from graphene_django.types import DjangoObjectType
from submission.models import Submission, SubmissionAttachInfo, SubmissionCase
from user.type import UserType
from problem.type import ProblemType
from judge.language import Language

class SubmissionAttachInfoType( DjangoObjectType ):
    class Meta:
        model = SubmissionAttachInfo
        only_fields = ( 'visibility' , 'cases_count' , 'time_cost' , 'memory_cost' )

class JudgeResultType( graphene.ObjectType ):
    status = graphene.String()
    compile_info = graphene.String()
    error_info = graphene.String()
    done = graphene.Boolean()

    def resolve_status( self , info , * args , ** kwargs ):
        return JudgeResult.value_of( self._result ).full

    def resolve_compile_info( self , info , is_self , is_privileage , * args , ** kwargs ):
        if is_self or is_privileage:
            return self.compile_info
        return ''
    
    def resolve_error_info( self , info , is_self , is_privileage , * args , ** kwargs ):
        if is_privileage:
            return self.error_info
        return ''
    
    def resolve_done( self , info , * args , ** kwargs ):
        return self.done

class SubmissionCaseType(DjangoObjectType):
    class Meta:
        model = SubmissionCase
        only_fields = ( 'time_cost' , 'memory_cost' )

class SubmissionCaseTypeList(graphene.ObjectType):
    cases_list = graphene.List( SubmissionCaseType )

class SubmissionType( graphene.ObjectType ):
    pk = graphene.ID()
    code = graphene.String()
    create_time = graphene.DateTime()
    user = graphene.Field( UserType )
    problem = graphene.Field( ProblemType )
    result = graphene.Field( JudgeResultType , is_self = graphene.Boolean() , is_privileage = graphene.Boolean() )
    attach_info = graphene.Field( SubmissionAttachInfoType )
    cases = graphene.Field( SubmissionCaseTypeList )
    language = graphene.String()

    def resolve_pk( self , info , * args , ** kwargs ):
        return self.pk

    def resolve_code( self , info , is_self , is_privileage , * args , ** kwargs ):
        if is_self or is_privileage:
            return self.code
        return ''
    
    def resolve_create_time( self , info , * args , ** kwargs ):
        return self.create_time
    
    def resolve_user( self , info , * args , ** kwargs ):
        return self.user

    def resolve_problem( self , info , * args , ** kwargs ):
        return self.problem

    def resolve_result( self , info , * args , ** kwargs ):
        return self.result
    
    def resolve_language( self , info , * args , ** kwargs ):
        return self.language.full
    
    def resolve_cases( self , info , * args , ** kwargs ):
        return list( SubmissionCase.objects.filter( submission = self ) )