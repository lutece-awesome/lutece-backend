import graphene
from annoying.functions import get_object_or_None
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils.datetime_safe import datetime
from graphql import ResolveInfo, GraphQLError

from contest.constant import PER_PAGE_COUNT, CLARIFICATION_PER_PAGE_COUNT
from contest.decorators import check_contest_permission
from contest.models import Contest, ContestSubmission, ContestTeamMember, \
    ContestClarification, ContestTeam
from contest.type import ContestListType, ContestType, ContestClarificationListType, \
    ContestRankingType, ContestTeamType
from submission.type import SubmissionListType


class Query(object):
    contest = graphene.Field(ContestType, pk=graphene.ID())
    contest_list = graphene.Field(ContestListType, page=graphene.Int(), filter=graphene.String())
    contest_submission_list = graphene.Field(SubmissionListType, pk=graphene.ID(), page=graphene.Int(),
                                             problem=graphene.String(), user=graphene.String(),
                                             judge_status=graphene.String(), language=graphene.String())
    contest_ranking_list = graphene.Field(ContestRankingType, pk=graphene.ID())
    contest_clarification_list = graphene.Field(ContestClarificationListType, pk=graphene.ID(), page=graphene.Int())
    contest_team = graphene.Field(ContestTeamType, pk=graphene.ID())
    contest_team_list = graphene.List(ContestTeamType, pk=graphene.ID())
    related_contest_team_list = graphene.List(ContestTeamType, pk=graphene.ID())

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
    def resolve_contest_submission_list(self: None, info: ResolveInfo, pk: graphene.ID(), page: graphene.Int(),
                                        **kwargs):
        judge_status = kwargs.get('judge_status')
        language = kwargs.get('language')
        problem = kwargs.get('problem')
        user = kwargs.get('user')
        contest = Contest.objects.get(pk=pk)
        privilege = info.context.user.has_perm('contest.view_contest')
        if datetime.now() < contest.settings.start_time and not privilege:
            return SubmissionListType(max_page=1, submission_list=[])
        status_list = ContestSubmission.objects.filter(contest=contest)
        if not privilege:
            team_member = get_object_or_None(ContestTeamMember, contest_team__contest=contest, user=info.context.user,
                                             confirmed=True)
            if not team_member or not team_member.contest_team.approved:
                return SubmissionListType(max_page=1, submission_list=[])
            status_list = status_list.filter(team=team_member.contest_team)
        status_list = status_list.order_by('-pk')
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

    @check_contest_permission
    def resolve_contest_ranking_list(self: None, info: ResolveInfo, pk: graphene.ID()):
        contest = Contest.objects.get(pk=pk)
        privilege = info.context.user.has_perm('contest.view_contest')
        if datetime.now() < contest.settings.start_time and not privilege:
            return ContestRankingType(submissions=[])
        submissions = ContestSubmission.objects.raw(
            '''
                SELECT 
                    submission_ptr_id,
                    contest_contestteam.name as team_name,
                    contest_contestteam.approved as team_approved,
                    submission_submission.create_time as create_time,
                    submission_submission.problem_id as problem_id,
                    submission_submission.result_id as result_id,
                    judge_judgeresult._result as judge_result
                FROM contest_contestsubmission
                LEFT JOIN contest_contestteam ON contest_contestsubmission.team_id = contest_contestteam.id
                LEFT JOIN submission_submission ON contest_contestsubmission.submission_ptr_id = submission_submission.id
                LEFT JOIN judge_judgeresult ON result_id = judge_judgeresult.id
                WHERE contest_contestsubmission.contest_id = (%s) and contest_contestsubmission.team_id IS NOT NULL
            ''',
            (pk,)
        )
        return ContestRankingType(submissions=submissions)

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

    def resolve_related_contest_team_list(self: None, info: ResolveInfo, pk: graphene.ID()):
        contest = Contest.objects.get(pk=pk)
        return map(lambda each: each.contest_team,
                   ContestTeamMember.objects.filter(contest_team__contest=contest, user=info.context.user))

    def resolve_contest_team(self: None, info: ResolveInfo, pk: graphene.ID()):
        return ContestTeam.objects.get(pk=pk)
