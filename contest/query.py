import graphene
from annoying.functions import get_object_or_None
from django.core.paginator import Paginator
from django.db.models import Prefetch, Q
from graphql import ResolveInfo, GraphQLError

from contest.constant import PER_PAGE_COUNT
from contest.decorators import check_contest_permission
from contest.models import ContestProblem, Contest, ContestSubmission, ContestTeam, ContestTeamMember
from contest.type import ContestRankingGroupType, ContestListType
from problem.type import ProblemType
from submission.type import SubmissionListType


class Query(object):
    contest_list = graphene.Field(ContestListType, page=graphene.Int(), filter=graphene.String())
    problem_list = graphene.List(ProblemType, pk=graphene.ID())
    team_submission_list = graphene.List(ProblemType, pk=graphene.ID(), team_pk=graphene.ID(), page=graphene.Int(),
                                         problem_pk=graphene.Int(), user=graphene.String(),
                                         judge_status=graphene.String(), language=graphene.String())
    ranking_list = graphene.List(ContestRankingGroupType, pk=graphene.ID())

    def resolve_contest_list(self: None, info: ResolveInfo, page: int, filter: str):
        contest_list = Contest.objects.all()
        privilege = info.context.user.has_perm('contest.view')
        if not privilege:
            contest_list = contest_list.filter(settings__disable=False)
        if filter:
            contest_list = contest_list.filter(Q(pk__contains=filter) | Q(title__icontains=filter))
        contest_list = contest_list.order_by('-pk')
        paginator = Paginator(contest_list, PER_PAGE_COUNT)
        return ContestListType(max_page=paginator.num_pages, contest_list=paginator.get_page(page))

    @check_contest_permission
    def resolve_problem_list(self: None, info: ResolveInfo, pk: graphene.ID()):
        return map(lambda each: each.problem, ContestProblem.objects.filter(contest=Contest.objects.get(pk=pk)))

    @check_contest_permission
    def resolve_team_submission_list(self: None, info: ResolveInfo, pk: graphene.ID(), team_pk: graphene.ID(),
                                     page: graphene.Int(),
                                     **kwargs):
        problem_pk = kwargs.get('problem_pk')
        user = kwargs.get('user')
        judge_status = kwargs.get('judge_status')
        language = kwargs.get('language')
        contest = Contest.objects.get(pk=pk)
        contest_team = ContestTeam.objects.get(pk=team_pk)
        privilege = info.context.user.has_perm('contest.view')
        status_list = ContestSubmission.objects.filter(contest=contest)
        if not privilege:
            if not get_object_or_None(ContestTeamMember, contest_team=contest_team, user=info.context.user):
                raise GraphQLError('Permission Denied')
            status_list = status_list.filter(team=contest_team)
        status_list = status_list.order_by('-pk')
        if not info.context.user.has_perm('problem.view'):
            status_list = status_list.filter(problem__disable=False)
        if not info.context.user.has_perm('user.view') or not info.context.user.has_perm('submission.view'):
            status_list = status_list.filter(user__is_staff=False)
        if pk:
            status_list = status_list.filter(pk=pk)
        if user:
            status_list = status_list.filter(user__username=user)
        if problem_pk:
            status_list = status_list.filter(problem__pk=problem_pk)
        if judge_status:
            status_list = status_list.filter(result___result=judge_status)
        if language:
            status_list = status_list.filter(_language=language)
        paginator = Paginator(status_list, PER_PAGE_COUNT)
        return SubmissionListType(max_page=paginator.num_pages, submission_list=paginator.get_page(page))

    @check_contest_permission
    def resolve_ranking_list(self: None, info: ResolveInfo, pk: graphene.ID()):
        contest = Contest.objects.get(pk=pk)
        status_list = ContestSubmission.objects.prefetch_related(
            Prefetch('team', ContestTeam.objects.filter(contest=contest), to_attr='team'))
        return [ContestRankingGroupType(name=each.team.name, team_ranking_list=each) for each in status_list]
