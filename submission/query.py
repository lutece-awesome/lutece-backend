import graphene
from django.core.paginator import Paginator
from graphql import ResolveInfo

from submission.constant import PER_PAGE_COUNT
from submission.models import Submission
from submission.type import SubmissionType, SubmissionListType


class Query(object):
    submission = graphene.Field(SubmissionType, pk=graphene.ID())
    submissionList = graphene.Field(SubmissionListType, page=graphene.Int(), pk=graphene.ID(), user=graphene.String(),
                                    problem=graphene.String(), judge_status=graphene.String(),
                                    language=graphene.String())

    def resolve_submission(self: None, info: ResolveInfo, pk: int):
        return Submission.objects.get(pk=pk)

    def resolve_submissionList(self: None, info: ResolveInfo, page: int, **kwargs):
        pk = kwargs.get('pk')
        user = kwargs.get('user')
        problem = kwargs.get('problem')
        judge_status = kwargs.get('judge_status')
        language = kwargs.get('language')
        status_list = Submission.objects.all().order_by('-pk')
        # Only consider base class
        status_list = status_list.filter(submission_type=0)
        if not info.context.user.has_perm('problem.view'):
            status_list = status_list.filter(problem__disable=False)
        if not info.context.user.has_perm('user.view') or not info.context.user.has_perm('submission.view'):
            status_list = status_list.filter(user__is_staff=False)
        if pk:
            status_list = status_list.filter(pk=pk)
        if user:
            status_list = status_list.filter(user__username=user)
        if problem:
            status_list = status_list.filter(problem__slug=problem)
        if judge_status:
            status_list = status_list.filter(result___result=judge_status)
        if language:
            status_list = status_list.filter(_language=language)
        paginator = Paginator(status_list, PER_PAGE_COUNT)
        return SubmissionListType(max_page=paginator.num_pages, submission_list=paginator.get_page(page))
