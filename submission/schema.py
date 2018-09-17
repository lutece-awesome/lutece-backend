import graphene
from graphene_django.types import DjangoObjectType
from annoying.functions import get_object_or_None
from problem.models import Problem
from .models import Submission, Judgeinfo
from graphql_jwt.decorators import login_required
from .tasks import Submission_task
from utils.schema import paginatorList
from submission.judge_result import Judge_result, Query_field
from user.models import User


class SubmissionType(DjangoObjectType):
    class Meta:
        model = Submission
        only_fields = ('user', 'problem', 'submission_id', 'language', 'judge_status', 'submit_time',
                       'case_number', 'completed', 'time_cost', 'memory_cost', 'code', 'judgererror_msg', 'compileerror_msg')

    color = graphene.String()
    failed_case = graphene.Int()

    def resolve_code(self, info, * args, ** kwargs):
        if self.user == info.context.user or info.context.user.has_perm('submission.view_all'):
            return self.code
        return ''

    def resolve_judgererror_msg(self, info, * args, ** kwargs):
        if info.context.user.has_perm('submission.view_all'):
            return self.judgererror_msg
        return ''

    def resolve_compileerror_msg(self, info, * args, ** kwargs):
        if self.user == info.context.user or info.context.user.has_perm('submission.view_all'):
            return self.compileerror_msg
        return ''

    def resolve_color(self, info, * args, ** kwargs):
        return Judge_result.get_judge_result(self.judge_status).value.color

    def resolve_failed_case(self, info, * args, ** kwargs):
        if Judge_result.get_judge_result(self.judge_status) in Query_field.failedcase_field.value:
            return Judgeinfo.objects.filter(submission=self).count()
        return None


class SubmissionListType(graphene.ObjectType):
    class Meta:
        interfaces = (paginatorList, )

    submissionList = graphene.List(SubmissionType)

class SubmissionStatistics( graphene.ObjectType ):
    ac = graphene.Int()
    tle = graphene.Int()
    ce = graphene.Int()
    wa = graphene.Int()
    re = graphene.Int()
    ole = graphene.Int()
    mle = graphene.Int()

    def __init__( self , * args , ** kwargs ):
        if 'user' in kwargs:
            self.user = kwargs['user']
        else:
            raise RuntimeError( 'User field is required' )

    def resolve_ac( self , info , * args , ** kwargs ):
        return Submission.objects.filter( user = self.user , judge_status = Judge_result.AC.value.full  ).count()

    def resolve_tle( self , info , * args , ** kwargs ):
        return Submission.objects.filter( user = self.user , judge_status = Judge_result.TLE.value.full  ).count()
    
    def resolve_ce( self , info , * args , ** kwargs ):
        return Submission.objects.filter( user = self.user , judge_status = Judge_result.CE.value.full  ).count()
    
    def resolve_wa( self , info , * args , ** kwargs ):
        return Submission.objects.filter( user = self.user , judge_status = Judge_result.WA.value.full  ).count()

    def resolve_re( self , info , * args , ** kwargs ):
        return Submission.objects.filter( user = self.user , judge_status = Judge_result.RE.value.full  ).count()

    def resolve_ole( self , info , * args , ** kwargs ):
        return Submission.objects.filter( user = self.user , judge_status = Judge_result.OLE.value.full  ).count()

    def resolve_mle( self , info , * args , ** kwargs ):
        return Submission.objects.filter( user = self.user , judge_status = Judge_result.MLE.value.full  ).count()
    


class SubmitSolution(graphene.Mutation):

    class Arguments:
        problemslug = graphene.String(required=True)
        code = graphene.String(required=True)
        language = graphene.String(required=True)

    pk = graphene.ID()

    @login_required
    def mutate(self, info, ** kwargs):
        from .form import SubmitSolutionForm
        from data_server.util import get_case_number
        from submission.judge_result import Judge_result
        from problem.util import InsSubmittimes
        from Lutece.settings import TASK_QUEUE
        SolutionForm = SubmitSolutionForm(kwargs)
        if SolutionForm.is_valid():
            values = SolutionForm.cleaned_data
            problem = get_object_or_None(Problem, slug=values['problemslug'])
            s = Submission(
                language=values['language'],
                user=info.context.user,
                problem=problem,
                case_number=get_case_number(problem.pk),
                judge_status=Judge_result.PD.value.full,
                code=values['code'])
            s.save()
            Submission_task.apply_async(
                args=(s.get_push_dict(),), queue=TASK_QUEUE)
            InsSubmittimes(problem.pk)
            return SubmitSolution(pk=s.pk)
        else:
            raise RuntimeError(SolutionForm.errors.as_json())


class Query(object):
    submission = graphene.Field(SubmissionType, pk=graphene.ID())
    submissionList = graphene.Field(SubmissionListType, page=graphene.Int(), date=graphene.String(), pk=graphene.ID(
    ), user=graphene.String(), problem=graphene.String(), judge_status=graphene.String(), language=graphene.String())

    def resolve_submission(self, info, pk):
        return Submission.objects.get(pk=pk)

    def resolve_submissionList(self, info, page, date, **kwargs):
        from django.core.paginator import Paginator
        from Lutece.config import PER_PAGE_COUNT
        pk = kwargs.get('pk')
        user = kwargs.get('user')
        problem = kwargs.get('problem')
        judge_status = kwargs.get('judge_status')
        language = kwargs.get('language')
        statuslist = Submission.objects.all()
        if not info.context.user.has_perm('problem.view_all'):
            statuslist = statuslist.filter(problem__visible=True)
        if not info.context.user.has_perm('submission.view_all'):
            statuslist = statuslist.filter(user__show=True)
        if pk is not None:
            statuslist = statuslist.filter(pk=pk)
        if user is not None:
            statuslist = statuslist.filter(user__display_name=user)
        if problem is not None:
            statuslist = statuslist.filter(problem__title=problem)
        if judge_status is not None:
            statuslist = statuslist.filter(judge_status=judge_status)
        if language is not None:
            statuslist = statuslist.filter(language=language)
        paginator = Paginator(statuslist, PER_PAGE_COUNT)
        return SubmissionListType(maxpage=paginator.num_pages, submissionList=paginator.get_page(page))


class Mutation(graphene.AbstractType):
    SubmitSolution = SubmitSolution.Field()
