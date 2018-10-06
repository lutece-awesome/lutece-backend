import graphene
from graphene_django.types import DjangoObjectType
from submission.models import Submission, SubmissionAttachInfo, SubmissionCase
from user.type import UserType
from problem.type import ProblemType
from judge.language import Language
from judge.result import JudgeResult
from utils.interface import PaginatorList

class SubmissionAttachInfoType( DjangoObjectType ):
    class Meta:
        model = SubmissionAttachInfo
        only_fields = ( 'visibility' , 'cases_count' , 'time_cost' , 'memory_cost' )

class JudgeResultType( graphene.ObjectType ):
    status = graphene.String()
    color = graphene.String()
    done = graphene.Boolean()
    compile_info = graphene.String()
    error_info = graphene.String()

    def resolve_status( self , info , * args , ** kwargs ):
        return self.result.full
    
    def resolve_color( self , info , * args , ** kwargs ):
        return self.result.color
    
    def resolve_done( self , info , * args , ** kwargs ):
        return self.done

    def resolve_compile_info( self , info , * args , ** kwargs ):
        usr = info.context.user
        if self.user == usr or usr.has_perm( 'Submission.view' ):
            return self.compile_info
        return ''

    def resolve_error_info( self , info , * args , ** kwargs ):
        if info.context.user.has_perm( 'Submission.view' ):
            return self.error_info
        return ''

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
    result = graphene.Field( JudgeResultType )
    attach_info = graphene.Field( SubmissionAttachInfoType )
    cases = graphene.Field( SubmissionCaseTypeList )
    language = graphene.String()
    failed_case = graphene.Int()

    def resolve_pk( self , info , * args , ** kwargs ):
        return self.pk

    def resolve_code( self , info , * args , ** kwargs ):
        usr = info.context.user
        if self.user == usr or usr.has_perm( 'Submission.view' ):
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
    
    def resolve_failed_case(self, info, * args, ** kwargs):
        if JudgeResult.is_failed( self.result ):
            return SubmissionCase.objects.filter( submission = self ).count()
        return None
    
    def resolve_cases( self , info , * args , ** kwargs ):
        return list( SubmissionCase.objects.filter( submission = self ) )

class SubmissionListType(graphene.ObjectType):
    class Meta:
        interfaces = (PaginatorList, )

    submission_list = graphene.List( SubmissionType )