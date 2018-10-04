import graphene
from django.core.paginator import Paginator
from submission.models import Submission
from submission.type import SubmissionType, SubmissionListType
from submission.constant import PER_PAGE_COUNT

class Query(object):
    submission = graphene.Field( SubmissionType, pk = graphene.ID() )
    submissionList = graphene.Field( SubmissionListType, page = graphene.Int(), date = graphene.String(), pk = graphene.ID(), user = graphene.String(), problem=graphene.String(), judge_status = graphene.String(), language = graphene.String() )

    def resolve_submission( self , info , pk ):
        return Submission.objects.get( pk = pk )

    def resolve_submissionList(self, info, page, date, **kwargs):
        pk = kwargs.get( 'pk' )
        user = kwargs.get( 'user' )
        problem = kwargs.get( 'problem' )
        judge_status = kwargs.get( 'judge_status' )
        language = kwargs.get( 'language' )
        statuslist = Submission.objects.all()
        if not info.context.user.has_perm( 'problem.view' ):
            statuslist = statuslist.filter( problem__disable = False )
        if not info.context.user.has_perm( 'user.view' ) or not info.context.user.has_perm( 'submission.view' ):
            statuslist = statuslist.filter( user__is_staff = False )
        if pk:
            statuslist = statuslist.filter( pk = pk )
        if user:
            statuslist = statuslist.filter( user__username = user )
        if problem:
            statuslist = statuslist.filter( problem__title = problem )
        if judge_status:
            statuslist = statuslist.filter( result___result = judge_status )
        if language:
            statuslist = statuslist.filter( _language = language )
        paginator = Paginator( statuslist , PER_PAGE_COUNT)
        return SubmissionListType( maxpage = paginator.num_pages , submission_list = paginator.get_page( page ) )