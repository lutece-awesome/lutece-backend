import graphene
from annoying.functions import get_object_or_None
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils.datetime_safe import datetime
from graphql import ResolveInfo, GraphQLError

from contest.constant import PER_PAGE_COUNT, CLARIFICATION_PER_PAGE_COUNT
from contest.decorators import check_contest_permission
from contest.models import ContestProblem, Contest, ContestSubmission, ContestTeamMember, \
    ContestClarification, ContestTeam
from contest.type import ContestListType, ContestType, ContestClarificationListType, \
    ContestProblemType, ContestRankingType, ContestTeamType
from submission.type import SubmissionListType


class Query(object):
    contest = graphene.Field(ContestType, pk=graphene.ID())
    contest_list = graphene.Field(ContestListType, page=graphene.Int(), filter=graphene.String())
    contest_problem_list = graphene.List(ContestProblemType, pk=graphene.ID())
    contest_submission_list = graphene.Field(SubmissionListType, pk=graphene.ID(), page=graphene.Int(),
                                             problem=graphene.String(), user=graphene.String(),
                                             judge_status=graphene.String(), language=graphene.String())
    contest_ranking_list = graphene.Field(ContestRankingType, pk=graphene.ID())
    contest_clarification_list = graphene.Field(ContestClarificationListType, pk=graphene.ID(), page=graphene.Int())
    contest_team_list = graphene.List(ContestTeamType, pk=graphene.ID())

    def resolve_contest(self: None, info: ResolveInfo, pk: int):
        contest_list = Contest.objects.all()
        privilege = info.context.user.has_perm('contest.view_contest')
        if not privilege:
            contest_list = contest_list.filter(settings__disable=False)
        return contest_list.get(pk=pk)

    def resolve_contest_list(self: None, info: ResolveInfo, page: int, filter: str):
        contest_list = Contest.objects.all()
        privilege = info.context.user.has_perm('contest.view_contest')
        if not privilege:
            contest_list = contest_list.filter(settings__disable=False)
        if filter:
            contest_list = contest_list.filter(Q(pk__contains=filter) | Q(title__icontains=filter))
        contest_list = contest_list.order_by('-pk')
        paginator = Paginator(contest_list, PER_PAGE_COUNT)
        return ContestListType(max_page=paginator.num_pages, contest_list=paginator.get_page(page))

    @check_contest_permission
    def resolve_contest_problem_list(self: None, info: ResolveInfo, pk: graphene.ID()):
        contest = Contest.objects.get(pk=pk)
        privilege = info.context.user.has_perm('contest.view_contest')
        if datetime.now() < contest.settings.start_time and not privilege:
            return []
        return map(lambda each: each.problem, ContestProblem.objects.filter(contest=contest))

    @check_contest_permission
    def resolve_contest_submission_list(self: None, info: ResolveInfo, pk: graphene.ID(), page: graphene.Int(),
                                        **kwargs):
        judge_status = kwargs.get('judge_status')
        language = kwargs.get('language')
        contest = Contest.objects.get(pk=pk)
        privilege = info.context.user.has_perm('contest.view_contest')
        if datetime.now() < contest.settings.start_time and not privilege:
            return SubmissionListType(max_page=1, submission_list=[])
        status_list = ContestSubmission.objects.filter(contest=contest)
        if not privilege:
            team_member = get_object_or_None(ContestTeamMember, contest_team__contest=contest, user=info.context.user)
            if not team_member:
                return SubmissionListType(max_page=1, submission_list=[])
            status_list = status_list.filter(team=team_member.contest_team)
        status_list = status_list.order_by('-pk')
        if not info.context.user.has_perm('problem.view'):
            status_list = status_list.filter(problem__disable=False)
        if not info.context.user.has_perm('user.view') or not info.context.user.has_perm('submission.view'):
            status_list = status_list.filter(user__is_staff=False)
        # if user:
        #     status_list = status_list.filter(user__username=user)
        # if problem:
        #     status_list = status_list.filter(problem__slug=problem)
        if judge_status:
            status_list = status_list.filter(result___result=judge_status)
        if language:
            status_list = status_list.filter(_language=language)
        paginator = Paginator(status_list, PER_PAGE_COUNT)
        return SubmissionListType(max_page=paginator.num_pages, submission_list=paginator.get_page(page))

    @check_contest_permission
    def resolve_contest_ranking_list(self: None, info: ResolveInfo, pk: graphene.ID()):
        contest = Contest.objects.get(pk=pk)
        privilege = info.context.user.has_perm('contest.view_contest')
        if datetime.now() < contest.settings.start_time and not privilege:
            return ContestRankingType(submissions=None, problems=None, meta=None)
        return ContestRankingType(
            submissions=ContestSubmission.objects.filter(Q(contest=contest) & ~Q(team=None) & Q(team__approved=True)),
            problems=map(lambda each: each.problem,
                         ContestProblem.objects.filter(contest=contest)),
            meta=contest)

    @check_contest_permission
    def resolve_contest_clarification_list(self: None, info: ResolveInfo, pk: graphene.ID(), page: graphene.Int()):
        contest = get_object_or_None(Contest, pk=pk)
        privilege = info.context.user.has_perm('contest.view_contest')
        if datetime.now() < contest.settings.start_time and not privilege:
            return ContestClarificationListType(max_page=1, contest_clarification_list=[])
        if not contest:
            raise GraphQLError('No such contest')
        clarification_list = ContestClarification.objects.filter(contest=contest)
        privilege = info.context.user.has_perm('contest.view_contestclarification')
        if not privilege:
            clarification_list = clarification_list.filter(disable=False)
        clarification_list = clarification_list.order_by('-create_time')
        paginator = Paginator(clarification_list, CLARIFICATION_PER_PAGE_COUNT)
        return ContestClarificationListType(max_page=paginator.num_pages,
                                            contest_clarification_list=paginator.get_page(page))

    def resolve_contest_team_list(self: None, info: ResolveInfo, pk: graphene.ID()):
        contest = Contest.objects.get(pk=pk)
        return ContestTeam.objects.filter(contest=contest)
