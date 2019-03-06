import graphene
import json
from django.utils import timezone
from graphql import ResolveInfo, GraphQLError
from graphql_jwt.decorators import permission_required

from contest.decorators import check_contest_permission
from contest.form import ContestForm, CreateContestClarificationForm
from contest.models import Contest, ContestSettings, ContestProblem, ContestClarification
from problem.models import Problem
from utils.function import assign


class CreateContest(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        note = graphene.String(required=True)
        disable = graphene.Boolean(required=True)
        start_time = graphene.DateTime(required=True)
        end_time = graphene.DateTime(required=True)
        max_team_member_number = graphene.Int(required=True)
        password = graphene.String(required=True)
        can_join_after_contest_begin = graphene.Boolean(required=True)
        join_need_approve = graphene.Boolean(required=True)
        problems = graphene.String(required=True)

    pk = graphene.ID()

    @permission_required('contest.add')
    def mutate(self, info: ResolveInfo, **kwargs):
        form = ContestForm(kwargs)
        if form.is_valid():
            values = form.cleaned_data
            values['start_time'] = timezone.localtime(values['start_time']).replace(tzinfo=None)
            values['end_time'] = timezone.localtime(values['end_time']).replace(tzinfo=None)
            problems = json.loads(values.get('problems'))
            contest = Contest()
            settings = ContestSettings()
            assign(settings, **values)
            settings.save()
            contest.title = values.get('title')
            contest.settings = settings
            contest.save()
            for each in problems:
                ContestProblem(
                    contest=contest,
                    problem=Problem.objects.get(pk=each)
                ).save()
            return CreateContest(pk=contest.pk)
        else:
            raise RuntimeError(form.errors.as_json())


class CreateContestClarification(graphene.Mutation):
    class Arguments:
        pk = graphene.ID(required=True)
        content = graphene.String(required=True)
        reply = graphene.ID(required=False)

    pk = graphene.ID()

    @check_contest_permission
    def mutate(self: None, info: ResolveInfo, **kwargs):
        form = CreateContestClarificationForm(kwargs)
        if form.is_valid():
            values = form.cleaned_data
            contest = Contest.objects.get(pk=values.get('pk'))
            reply = values.get('reply')
            if reply:
                reply = ContestClarification.objects.get(pk=reply)
            comment = ContestClarification.objects.create(
                contest=contest,
                content=values.get('content'),
                reply=reply,
                author=info.context.user
            )
            return CreateContestClarification(pk=comment.pk)
        else:
            raise GraphQLError(form.errors.as_json())


class Mutation(graphene.AbstractType):
    create_contest = CreateContest.Field()
    create_contest_clarification = CreateContestClarification.Field()
