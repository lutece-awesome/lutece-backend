import graphene
from graphene_django.types import DjangoObjectType
from graphql import ResolveInfo
from typing import List

from judge.result import JudgeResult
from submission.models import Submission
from user.models import Solve, User


class UserSolveType(DjangoObjectType):
    class Meta:
        model = Solve
        only_fields = 'status'

    pk = graphene.ID()
    slug = graphene.String()

    def resolve_pk(self: Solve, info: ResolveInfo) -> int:
        return self.problem.pk

    def resolve_slug(self: Solve, info: ResolveInfo) -> int:
        return self.problem.slug


class UserSubmissionStatisticsType(graphene.ObjectType):
    ac = graphene.Int()
    tle = graphene.Int()
    ce = graphene.Int()
    wa = graphene.Int()
    re = graphene.Int()
    ole = graphene.Int()
    mle = graphene.Int()
    ratio = graphene.Float()
    solve = graphene.List(UserSolveType)

    __slots__ = (
        'user'  # type: User
    )

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def resolve_ac(self, info: ResolveInfo) -> int:
        return Submission.objects.filter(user=self.user, result___result=JudgeResult.AC.full).count()

    def resolve_tle(self, info: ResolveInfo) -> int:
        return Submission.objects.filter(user=self.user, result___result=JudgeResult.TLE.full).count()

    def resolve_ce(self, info: ResolveInfo) -> int:
        return Submission.objects.filter(user=self.user, result___result=JudgeResult.CE.full).count()

    def resolve_wa(self, info: ResolveInfo) -> int:
        return Submission.objects.filter(user=self.user, result___result=JudgeResult.WA.full).count()

    def resolve_re(self, info: ResolveInfo) -> int:
        return Submission.objects.filter(user=self.user, result___result=JudgeResult.RE.full).count()

    def resolve_ole(self, info: ResolveInfo) -> int:
        return Submission.objects.filter(user=self.user, result___result=JudgeResult.OLE.full).count()

    def resolve_mle(self, info: ResolveInfo) -> int:
        return Submission.objects.filter(user=self.user, result___result=JudgeResult.MLE.full).count()

    def resolve_ratio(self, info: ResolveInfo) -> float:
        ac = self.resolve_ac(info)
        _all = Submission.objects.filter(user=self.user).count()
        return ac / _all if _all else 0

    def resolve_solve(self, info: ResolveInfo) -> List:
        return list(Solve.objects.filter(user=self.user).order_by('problem__pk'))
